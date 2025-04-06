from typing import List, Optional
from datetime import date
from pydantic import BaseModel

type datetimedate = date


class LanguageUsage(BaseModel):
    name: Optional[str] = None
    total_engaged_users: Optional[int] = None
    total_code_suggestions: Optional[int] = None
    total_code_acceptances: Optional[int] = None
    total_code_lines_suggested: Optional[int] = None
    total_code_lines_accepted: Optional[int] = None


class ModelBase(BaseModel):
    name: Optional[str] = None
    is_custom_model: Optional[bool] = None
    custom_model_training_date: Optional[date] = None


class CompletionModel(ModelBase):
    total_engaged_users: Optional[int] = None
    languages: Optional[List[LanguageUsage]] = None


class ChatModel(ModelBase):
    total_engaged_users: Optional[int] = None
    total_chats: Optional[int] = None
    total_chat_insertion_events: Optional[int] = None
    total_chat_copy_events: Optional[int] = None


class PullRequestModel(ModelBase):
    total_engaged_users: Optional[int] = None
    total_pr_summaries_created: Optional[int] = None


class EditorCompletionUsage(BaseModel):
    name: Optional[str] = None
    total_engaged_users: Optional[int] = None
    models: Optional[List[CompletionModel]] = None


class EditorChatUsage(BaseModel):
    name: Optional[str] = None
    total_engaged_users: Optional[int] = None
    models: Optional[List[ChatModel]] = None


class RepositoryUsage(BaseModel):
    name: Optional[str] = None
    total_engaged_users: Optional[int] = None
    models: Optional[List[PullRequestModel]] = None


class CopilotIDECodeCompletions(BaseModel):
    total_engaged_users: Optional[int] = None
    languages: Optional[List[LanguageUsage]] = None
    editors: Optional[List[EditorCompletionUsage]] = None


class CopilotIDEChat(BaseModel):
    total_engaged_users: Optional[int] = None
    editors: Optional[List[EditorChatUsage]] = None


class CopilotDotcomChat(BaseModel):
    total_engaged_users: Optional[int] = None
    models: Optional[List[ChatModel]] = None


class CopilotDotcomPullRequests(BaseModel):
    total_engaged_users: Optional[int] = None
    repositories: Optional[List[RepositoryUsage]] = None


class CopilotMetricsEntry(BaseModel):
    date: Optional[datetimedate] = None
    total_active_users: Optional[int] = None
    total_engaged_users: Optional[int] = None
    copilot_ide_code_completions: Optional[CopilotIDECodeCompletions] = None
    copilot_ide_chat: Optional[CopilotIDEChat] = None
    copilot_dotcom_chat: Optional[CopilotDotcomChat] = None
    copilot_dotcom_pull_requests: Optional[CopilotDotcomPullRequests] = None
