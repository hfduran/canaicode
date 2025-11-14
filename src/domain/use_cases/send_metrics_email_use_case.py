from typing import Any, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.domain.entities.value_objects.enums.period import Period
from src.domain.entities.value_objects.enums.productivity_metric import Productivity_metric
from src.domain.use_cases.get_calculated_metrics_use_case import GetCalculatedMetricsUseCase
from src.domain.use_cases.get_copilot_metrics_by_language_use_case import GetCopilotMetricsByLanguageUseCase
from src.domain.use_cases.get_copilot_metrics_by_period_use_case import GetCopilotMetricsByPeriodUseCase
from src.domain.use_cases.get_copilot_users_metrics_use_case import GetCopilotUsersMetricsUseCase
from src.infrastructure.database.report_config.postgre.report_config_repository import ReportConfigRepository
from src.infrastructure.logger.logger_config import logger


class SendMetricsEmailUseCase:
    def __init__(
        self,
        report_config_repository: ReportConfigRepository,
        get_calculated_metrics_use_case: GetCalculatedMetricsUseCase,
        get_copilot_metrics_by_language_use_case: GetCopilotMetricsByLanguageUseCase,
        get_copilot_metrics_by_period_use_case: GetCopilotMetricsByPeriodUseCase,
        get_copilot_users_metrics_use_case: GetCopilotUsersMetricsUseCase,
        mail_name: str,
        mail_password: str
    ) -> None:
        self.report_config_repository = report_config_repository
        self.get_calculated_metrics_use_case = get_calculated_metrics_use_case
        self.get_copilot_metrics_by_language_use_case = get_copilot_metrics_by_language_use_case
        self.get_copilot_metrics_by_period_use_case = get_copilot_metrics_by_period_use_case
        self.get_copilot_users_metrics_use_case = get_copilot_users_metrics_use_case
        self.mail_name = mail_name
        self.mail_password = mail_password

    def execute(self) -> None:
        report_configs = self.report_config_repository.list()

        for report_config in report_configs:
            print(report_config.emails)
            try:
              today = datetime(2025, 5, 1) # datetime.now()
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
              self.send_email(report_config.emails, graphs)
            except Exception as e:
                logger.error(f"Error during send weekly email: {e}")

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

    def send_email(self, emails: List[str], graphs: List[Tuple[str, io.BytesIO]]) -> None:
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
