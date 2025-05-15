from datetime import date
from typing import List

from pydantic import BaseModel

type datetimedate = date


class LanguageUsage(BaseModel):
    name: str
    total_engaged_users: int
    total_code_suggestions: int
    total_code_acceptances: int
    total_code_lines_suggested: int
    total_code_lines_accepted: int


class ModelBase(BaseModel):
    name: str
    is_custom_model: bool
    custom_model_training_date: date


class CompletionModel(ModelBase):
    total_engaged_users: int
    languages: List[LanguageUsage]


class ChatModel(ModelBase):
    total_engaged_users: int
    total_chats: int
    total_chat_insertion_events: int
    total_chat_copy_events: int


class PullRequestModel(ModelBase):
    total_engaged_users: int
    total_pr_summaries_created: int


class EditorCompletionUsage(BaseModel):
    name: str
    total_engaged_users: int
    models: List[CompletionModel]


class EditorChatUsage(BaseModel):
    name: str
    total_engaged_users: int
    models: List[ChatModel]


class RepositoryUsage(BaseModel):
    name: str
    total_engaged_users: int
    models: List[PullRequestModel]


class CopilotIDECodeCompletions(BaseModel):
    total_engaged_users: int
    languages: List[LanguageUsage]
    editors: List[EditorCompletionUsage]


class CopilotIDEChat(BaseModel):
    total_engaged_users: int
    editors: List[EditorChatUsage]


class CopilotDotcomChat(BaseModel):
    total_engaged_users: int
    models: List[ChatModel]


class CopilotDotcomPullRequests(BaseModel):
    total_engaged_users: int
    repositories: List[RepositoryUsage]


class CopilotMetricsEntryDTO(BaseModel):
    date: str
    total_active_users: int
    total_engaged_users: int
    copilot_ide_code_completions: CopilotIDECodeCompletions
    copilot_ide_chat: CopilotIDEChat
    copilot_dotcom_chat: CopilotDotcomChat
    copilot_dotcom_pull_requests: CopilotDotcomPullRequests
