import time
import requests
from typing import Any, Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import io
import smtplib
from jose import jwt
from cryptography.fernet import Fernet
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from src.domain.entities.github_app import GitHubApp
from src.domain.entities.report_config import ReportConfig
from src.domain.entities.value_objects.enums.period import Period
from src.domain.entities.value_objects.enums.productivity_metric import Productivity_metric
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.infrastructure.database.github_apps.postgre.github_apps_repository import GitHubAppsRepository
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository
from src.infrastructure.logger.logger_config import logger


class SendMetricsEmailUseCase:
    def __init__(
        self,
        report_config_repository: ReportConfigRepository,
        github_apps_repository: GitHubAppsRepository,
        get_calculated_metrics_use_case: GetCalculatedMetricsUseCase,
        get_copilot_metrics_by_language_use_case: GetCopilotMetricsByLanguageUseCase,
        get_copilot_metrics_by_period_use_case: GetCopilotMetricsByPeriodUseCase,
        get_copilot_users_metrics_use_case: GetCopilotUsersMetricsUseCase,
        mail_name: str,
        mail_password: str,
        encryption_key: str,
    ) -> None:
        self.report_config_repository = report_config_repository
        self.github_apps_repository = github_apps_repository
        self.get_calculated_metrics_use_case = get_calculated_metrics_use_case
        self.get_copilot_metrics_by_language_use_case = get_copilot_metrics_by_language_use_case
        self.get_copilot_metrics_by_period_use_case = get_copilot_metrics_by_period_use_case
        self.get_copilot_users_metrics_use_case = get_copilot_users_metrics_use_case
        self.mail_name = mail_name
        self.mail_password = mail_password
        self.fernet = Fernet(encryption_key.encode())

    def execute(self) -> None:
        report_configs = self.report_config_repository.list()

        for report_config in report_configs:
            try:
              github_app = self.github_apps_repository.find_by_user_id(report_config.user_id)
              today = datetime.now()
              graphs: List[Tuple[str, io.BytesIO]] = []
              inactive_users: List[str] = []
              if report_config.period == Period.DAILY:
                 graphs, inactive_users = self.make_daily_graphs(report_config, today, github_app)
              elif report_config.period == Period.WEEK and today.weekday() == 0:
                 graphs, inactive_users = self.make_weekly_graphs(report_config, today, github_app)
              elif report_config.period == Period.MONTH and today.day == 1:
                 graphs, inactive_users = self.make_monthly_graphs(report_config, today, github_app)
              elif report_config.period == Period.QUARTER and today.month in [1, 4, 7, 10] and today.day == 1:
                 graphs, inactive_users = self.make_quarterly_graphs(report_config, today, github_app)
              if len(graphs) > 0:
                self.send_email(report_config.emails, graphs, inactive_users)
            except Exception as e:
                logger.error(f"Error during send weekly email: {e}")

    def make_daily_graphs(self, report_config: ReportConfig, today: datetime, github_app: GitHubApp | None) -> Tuple[List[Tuple[str, io.BytesIO]], List[str]]:
      ten_weeks_ago = today - timedelta(weeks=10)
      last_ten_weeks_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.WEEK, Productivity_metric.code_lines, ten_weeks_ago, today)
      six_months_ago = today - relativedelta(months=6)
      last_six_months_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.MONTH, Productivity_metric.code_lines, six_months_ago, today)
      one_week_ago = today - timedelta(weeks=1)
      last_week_copilot_metrics_by_language = self.get_copilot_metrics_by_language_use_case.execute(report_config.user_id, one_week_ago, today)
      last_week_copilot_metrics_by_day = self.get_copilot_metrics_by_period_use_case.execute(report_config.user_id, Period.DAILY, one_week_ago, today)
      last_week_copilot_users_metrics = self.get_copilot_users_metrics_use_case.execute(report_config.user_id, one_week_ago, today)
      graphs: List[Tuple[str, io.BytesIO]] = []
      if len(last_ten_weeks_productivity_metrics.data) > 0:
        graphs.append(('last_ten_weeks_productivity.png', self.make_graph(last_ten_weeks_productivity_metrics.data, 'Last ten weeks productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_six_months_productivity_metrics.data) > 0:
        graphs.append(('last_six_months_productivity.png', self.make_graph(last_six_months_productivity_metrics.data, 'Last six months productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_week_copilot_metrics_by_language) > 0:
        graphs.append(('last_week_copilot_metrics_by_language.png', self.make_graph(last_week_copilot_metrics_by_language, 'Last week copilot metrics by language', 'language', ['lines_suggested', 'lines_accepted'], 'Language', 'Lines suggested/accepted'))) # type: ignore
      if len(last_week_copilot_metrics_by_day) > 0:
        graphs.append(('last_week_copilot_metrics_by_day.png', self.make_graph(last_week_copilot_metrics_by_day, 'Last week copilot metrics by day', 'period_initial_date', ['total_code_acceptances', 'total_lines_accepted'], 'Date', 'Number of acceptances/Total lines accepted'))) # type: ignore
      if len(last_week_copilot_users_metrics) > 0:
        graphs.append(('last_week_copilot_users_metrics.png', self.make_graph(last_week_copilot_users_metrics, 'Last week copilot users metrics', 'date', ['total_code_assistant_users', 'total_chat_users'], 'Date', 'Total users of code assistant/chat'))) # type: ignore
      inactive_users: List[str] = []
      if github_app:
         inactive_users = self.get_inactive_users(github_app, 30)
      return graphs, inactive_users

    def make_weekly_graphs(self, report_config: ReportConfig, today: datetime, github_app: GitHubApp | None) -> Tuple[List[Tuple[str, io.BytesIO]], List[str]]:
      ten_weeks_ago = today - timedelta(weeks=10)
      last_ten_weeks_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.WEEK, Productivity_metric.code_lines, ten_weeks_ago, today)
      six_months_ago = today - relativedelta(months=6)
      last_six_months_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.MONTH, Productivity_metric.code_lines, six_months_ago, today)
      one_week_ago = today - timedelta(weeks=1)
      last_week_copilot_metrics_by_language = self.get_copilot_metrics_by_language_use_case.execute(report_config.user_id, one_week_ago, today)
      last_week_copilot_metrics_by_day = self.get_copilot_metrics_by_period_use_case.execute(report_config.user_id, Period.DAILY, one_week_ago, today)
      last_week_copilot_users_metrics = self.get_copilot_users_metrics_use_case.execute(report_config.user_id, one_week_ago, today)
      graphs: List[Tuple[str, io.BytesIO]] = []
      if len(last_ten_weeks_productivity_metrics.data) > 0:
        graphs.append(('last_ten_weeks_productivity.png', self.make_graph(last_ten_weeks_productivity_metrics.data, 'Last ten weeks productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_six_months_productivity_metrics.data) > 0:
        graphs.append(('last_six_months_productivity.png', self.make_graph(last_six_months_productivity_metrics.data, 'Last six months productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_week_copilot_metrics_by_language) > 0:
        graphs.append(('last_week_copilot_metrics_by_language.png', self.make_graph(last_week_copilot_metrics_by_language, 'Last week copilot metrics by language', 'language', ['lines_suggested', 'lines_accepted'], 'Language', 'Lines suggested/accepted'))) # type: ignore
      if len(last_week_copilot_metrics_by_day) > 0:
        graphs.append(('last_week_copilot_metrics_by_day.png', self.make_graph(last_week_copilot_metrics_by_day, 'Last week copilot metrics by day', 'period_initial_date', ['total_code_acceptances', 'total_lines_accepted'], 'Date', 'Number of acceptances/Total lines accepted'))) # type: ignore
      if len(last_week_copilot_users_metrics) > 0:
        graphs.append(('last_week_copilot_users_metrics.png', self.make_graph(last_week_copilot_users_metrics, 'Last week copilot users metrics', 'date', ['total_code_assistant_users', 'total_chat_users'], 'Date', 'Total users of code assistant/chat'))) # type: ignore
      inactive_users: List[str] = []
      if github_app:
         inactive_users = self.get_inactive_users(github_app, 30)
      return graphs, inactive_users
    
    def make_monthly_graphs(self, report_config: ReportConfig, today: datetime, github_app: GitHubApp | None) -> Tuple[List[Tuple[str, io.BytesIO]], List[str]]:
      ten_weeks_ago = today - timedelta(weeks=10)
      last_ten_weeks_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.WEEK, Productivity_metric.code_lines, ten_weeks_ago, today)
      six_months_ago = today - relativedelta(months=6)
      last_six_months_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.MONTH, Productivity_metric.code_lines, six_months_ago, today)
      one_month_ago = today - relativedelta(months=1)
      last_month_copilot_metrics_by_language = self.get_copilot_metrics_by_language_use_case.execute(report_config.user_id, one_month_ago, today)
      last_month_copilot_metrics_by_week = self.get_copilot_metrics_by_period_use_case.execute(report_config.user_id, Period.WEEK, one_month_ago, today)
      last_month_copilot_users_metrics = self.get_copilot_users_metrics_use_case.execute(report_config.user_id, one_month_ago, today)
      graphs: List[Tuple[str, io.BytesIO]] = []
      if len(last_ten_weeks_productivity_metrics.data) > 0:
        graphs.append(('last_ten_weeks_productivity.png', self.make_graph(last_ten_weeks_productivity_metrics.data, 'Last ten weeks productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_six_months_productivity_metrics.data) > 0:
        graphs.append(('last_six_months_productivity.png', self.make_graph(last_six_months_productivity_metrics.data, 'Last six months productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_month_copilot_metrics_by_language) > 0:
        graphs.append(('last_month_copilot_metrics_by_language.png', self.make_graph(last_month_copilot_metrics_by_language, 'Last month copilot metrics by language', 'language', ['lines_suggested', 'lines_accepted'], 'Language', 'Lines suggested/accepted'))) # type: ignore
      if len(last_month_copilot_metrics_by_week) > 0:
        graphs.append(('last_month_copilot_metrics_by_week.png', self.make_graph(last_month_copilot_metrics_by_week, 'Last month copilot metrics by week', 'period_initial_date', ['total_code_acceptances', 'total_lines_accepted'], 'Date', 'Number of acceptances/Total lines accepted'))) # type: ignore
      if len(last_month_copilot_users_metrics) > 0:
        graphs.append(('last_month_copilot_users_metrics.png', self.make_graph(last_month_copilot_users_metrics, 'Last month copilot users metrics', 'date', ['total_code_assistant_users', 'total_chat_users'], 'Date', 'Total users of code assistant/chat'))) # type: ignore
      inactive_users: List[str] = []
      if github_app:
         inactive_users = self.get_inactive_users(github_app, 30)
      return graphs, inactive_users
    
    def make_quarterly_graphs(self, report_config: ReportConfig, today: datetime, github_app: GitHubApp | None) -> Tuple[List[Tuple[str, io.BytesIO]], List[str]]:
      ten_weeks_ago = today - timedelta(weeks=10)
      last_ten_weeks_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.WEEK, Productivity_metric.code_lines, ten_weeks_ago, today)
      six_months_ago = today - relativedelta(months=6)
      last_six_months_productivity_metrics = self.get_calculated_metrics_use_case.execute(report_config.user_id, Period.MONTH, Productivity_metric.code_lines, six_months_ago, today)
      one_month_ago = today - relativedelta(months=1)
      one_quarter_ago = today - relativedelta(months=3)
      last_quarter_copilot_metrics_by_language = self.get_copilot_metrics_by_language_use_case.execute(report_config.user_id, one_quarter_ago, today)
      last_quarter_copilot_metrics_by_week = self.get_copilot_metrics_by_period_use_case.execute(report_config.user_id, Period.WEEK, one_quarter_ago, today)
      last_month_copilot_users_metrics = self.get_copilot_users_metrics_use_case.execute(report_config.user_id, one_month_ago, today)
      graphs: List[Tuple[str, io.BytesIO]] = []
      if len(last_ten_weeks_productivity_metrics.data) > 0:
        graphs.append(('last_ten_weeks_productivity.png', self.make_graph(last_ten_weeks_productivity_metrics.data, 'Last ten weeks productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_six_months_productivity_metrics.data) > 0:
        graphs.append(('last_six_months_productivity.png', self.make_graph(last_six_months_productivity_metrics.data, 'Last six months productivity', 'initial_date', ['net_changed_lines', 'net_changed_lines_by_copilot'], 'Date', 'Changed lines total/copilot'))) # type: ignore
      if len(last_quarter_copilot_metrics_by_language) > 0:
        graphs.append(('last_quarter_copilot_metrics_by_language.png', self.make_graph(last_quarter_copilot_metrics_by_language, 'Last quarter copilot metrics by language', 'language', ['lines_suggested', 'lines_accepted'], 'Language', 'Lines suggested/accepted'))) # type: ignore
      if len(last_quarter_copilot_metrics_by_week) > 0:
        graphs.append(('last_quarter_copilot_metrics_by_week.png', self.make_graph(last_quarter_copilot_metrics_by_week, 'Last quarter copilot metrics by week', 'period_initial_date', ['total_code_acceptances', 'total_lines_accepted'], 'Date', 'Number of acceptances/Total lines accepted'))) # type: ignore
      if len(last_month_copilot_users_metrics) > 0:
        graphs.append(('last_month_copilot_users_metrics.png', self.make_graph(last_month_copilot_users_metrics, 'Last month copilot users metrics', 'date', ['total_code_assistant_users', 'total_chat_users'], 'Date', 'Total users of code assistant/chat'))) # type: ignore
      inactive_users: List[str] = []
      if github_app:
         inactive_users = self.get_inactive_users(github_app, 90)
      return graphs, inactive_users

    def make_graph(self, data: List[Any], title: str, line_name: str, colum_names: List[str], line_label: str, column_label: str) -> io.BytesIO:
      dict_data = [vars(d) if not isinstance(d, dict) else d for d in data]  # type: ignore
      df = pd.DataFrame(dict_data)

      if line_name not in df.columns:
          raise ValueError(f"Column '{line_name}' not found in data")
      for col in colum_names:
          if col not in df.columns:
              raise ValueError(f"Column '{col}' not found in data")

      fig, ax = plt.subplots(figsize=(12, 6)) # type: ignore

      parsed = pd.to_datetime(df[line_name], errors='coerce', utc=False)

      is_datetime = parsed.notna().any()

      if is_datetime:
          try:
              parsed = parsed.dt.tz_convert(None)
          except Exception:
              pass
          parsed = parsed.dt.normalize()

          df[line_name] = parsed
          df = df.sort_values(by=line_name).reset_index(drop=True)

          df.plot(x=line_name, y=colum_names, kind='bar', legend=True, ax=ax)

          labels = []
          for d in df[line_name]:
              if pd.isna(d):
                  labels.append("") # type: ignore
              else:
                  labels.append(d.strftime("%d/%m/%Y")) # type: ignore

          ticks = list(range(len(labels))) # type: ignore
          ax.set_xticks(ticks) # type: ignore
          ax.set_xticklabels(labels) # type: ignore
          if len(labels) > 30: # type: ignore
              step = max(1, len(labels) // 15) # type: ignore
              for i, lbl in enumerate(ax.get_xticklabels()):
                  if i % step != 0:
                      lbl.set_visible(False)
      else:
          df[line_name] = df[line_name].astype(str)
          df.plot(x=line_name, y=colum_names, kind='bar', legend=True, ax=ax)

      ax.set_title(title) # type: ignore
      ax.set_xlabel(line_label) # type: ignore
      ax.set_ylabel(column_label) # type: ignore

      for lbl in ax.get_xticklabels():
          lbl.set_rotation(45)
          lbl.set_ha('right') # type: ignore

      plt.tight_layout()

      img_bytes = io.BytesIO()
      plt.savefig(img_bytes, format='png', bbox_inches='tight') # type: ignore
      img_bytes.seek(0)
      plt.close(fig)
      return img_bytes

    def send_email(self, emails: List[str], graphs: List[Tuple[str, io.BytesIO]], inactive_users: List[str]) -> None:
      msg = EmailMessage()
      msg['Subject'] = 'Metrics Report'
      msg['From'] = self.mail_name
      msg['To'] = ", ".join(emails)

      msg.set_content("Seu cliente de e-mail não suporta HTML.")

      graphs_html = ""
      for index, (name, _) in enumerate(graphs):
          cid = f"graph{index}"

          graphs_html += f"""
          <div style="margin:25px 0;">
              <h3 style="color:#2a4d8f; margin-bottom:5px;">{name}</h3>
              <img src="cid:{cid}" alt="{name}" style="max-width:100%; border-radius:6px;">
          </div>
          """

      inactive_users_html = ""
      if inactive_users:
          inactive_users_list = "".join(f"<li>{user}</li>" for user in inactive_users)
          inactive_users_html = f"""
          <div style="padding:15px; margin-top:30px; background:#fff6f6; border:1px solid #ffa39e; border-radius:6px;">
              <h3 style="margin-top:0; color:#cf1322;">⚠️ Usuários inativos nos últimos 30 dias</h3>
              <p style="margin:0 0 10px;">Os seguintes usuários não tiveram atividade registrada recentemente:</p>
              <ul style="margin:0; padding-left:20px; color:#555; font-size:14px;">
                  {inactive_users_list}
              </ul>
          </div>
          """

      html = f"""
      <!DOCTYPE html>
      <html>
        <body style="margin:0; padding:0; background-color:#f4f4f7; font-family:Arial, sans-serif;">

          <div style="max-width:600px; margin:0 auto; background:#ffffff; padding:30px; border-radius:8px;">

            <h1 style="color:#2a4d8f; text-align:center; margin-bottom:10px;">
              📊 Metrics Report
            </h1>

            <p style="font-size:16px; color:#444; text-align:center; margin-top:0;">
              Segue abaixo o relatório da última semana contendo métricas e gráficos.
            </p>

            <hr style="border:none; border-top:1px solid #ddd; margin:20px 0;">

            <div style="font-size:15px; color:#333;">
              <p>Olá,</p>
              <p>Confira abaixo os gráficos gerados automaticamente pelo sistema:</p>
            </div>

            {graphs_html}

            {inactive_users_html}

            <hr style="border:none; border-top:1px solid #ddd; margin:30px 0;">

            <p style="font-size:14px; color:#666; text-align:center;">
              Este e-mail foi enviado automaticamente pelo sistema de relatórios.
            </p>

          </div>

        </body>
      </html>
      """

      msg.add_alternative(html, subtype='html')

      html_part = msg.get_payload()[-1] # type: ignore

      for index, (_, img_bytes) in enumerate(graphs):
          cid = f"graph{index}"
          img_bytes.seek(0)

          html_part.add_related( # type: ignore
              img_bytes.read(),
              maintype='image',
              subtype='png',
              cid=cid,
              filename=f"{cid}.png"
          )

      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
          smtp.login(self.mail_name, self.mail_password)
          smtp.send_message(msg)

    def get_inactive_users(self, github_app: GitHubApp, days_inactive: int) -> List[str]:
      try:
        now = int(time.time())
        
        private_key = self.fernet.decrypt(github_app.private_key_encrypted.encode()).decode()
        
        payload: Dict[str, str | int] = {
            "iat": now,
            "exp": now + (10 * 60),  # JWT valid for 10 minutes
            "iss": github_app.app_id,
        }
        jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }
        token_url = f"https://api.github.com/app/installations/{github_app.installation_id}/access_tokens"
        token_response = requests.post(token_url, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["token"]

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        }
        seats_url = f"https://api.github.com/orgs/{github_app.organization_name}/copilot/billing/seats"
        seats_response = requests.get(seats_url, headers=headers)
        seats_response.raise_for_status()
        data = seats_response.json()

        inactive_users: List[str] = []
        limit = datetime.now(timezone.utc) - timedelta(days=days_inactive)

        for seat in data.get("seats", []):
          last_active = seat.get("last_activity_at")
          if last_active:
              last_active_dt = datetime.fromisoformat(last_active.replace("Z", "+00:00"))
              if last_active_dt < limit:
                  inactive_users.append(seat["user"]["login"])

        return inactive_users
      except Exception as e:
        logger.error(f"Error fetching inactive users: {e}")
        return []


