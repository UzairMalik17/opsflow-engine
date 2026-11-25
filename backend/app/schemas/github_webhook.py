from pydantic import BaseModel, ConfigDict


class GitHubRepository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    full_name: str


class GithubSender(BaseModel):
    model_config = ConfigDict(extra="ignore")

    login: str


class GithubIssue(BaseModel):
    model_config = ConfigDict(extra="ignore")

    number: int
    title: str


class GithubWebhookPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    action: str | None = None
    repository: GitHubRepository
    issue: GithubIssue | None = None
    sender: GithubSender | None = None
