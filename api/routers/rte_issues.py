from fastapi import status, Depends, APIRouter, Response, Query
from ..validators import val_auth, val_issues
from ratelimit import limits, sleep_and_retry
from ..oauth2.oauth2 import get_current_user
from fastapi.responses import JSONResponse
from .metadata import md_issues
from .. config import settings
from loguru import logger
import pendulum as ptime
from typing import List
import httpx


LIMIT_SECONDS = 10
LIMIT_CALLS = 20


token = settings.GIT_TOKEN
tz = ptime.timezone('America/Denver')


router = APIRouter(prefix="/issues", tags=['Issues'])


def git_assignee(name: str):
    match name:
        case 'Adam':
            return 'oso1248'
        case _:
            return False


@router.post("", status_code=status.HTTP_201_CREATED, response_model=val_issues.IssuesCreateGet, description=md_issues.create)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
async def issues_create(issue: val_issues.IssuesCreate, assignee: str = Query(None, enum=['Adam']),  current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    try:
        assignee = git_assignee(assignee)

        if not assignee:
            return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT, content={'detail': "cannot find assignee"})

        issue = issue.dict()
        issue['body'] = issue['body'] + f'\n\n\n{current_user.eid}'
        issue['assignee'] = assignee

        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.github.com/repos/oso1248/db_material/issues", headers={'Authorization': f'Bearer {token}'}, json=issue)

        response = response.json()

        if len(response) == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        response['owner'] = response['assignee']['login']
        response['label'] = response['labels'][0]['name']

        return response

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("", response_model=List[val_issues.IssuesCreateGet], description=md_issues.get)
@logger.catch()
@sleep_and_retry
@limits(calls=LIMIT_CALLS, period=LIMIT_SECONDS)
async def issues_get(state: str = Query('open', enum=['open', 'closed']), label: str = Query('', enum=['bug', 'design', 'enhancement', 'question']), current_user: val_auth.UserCurrent = Depends(get_current_user)):

    if current_user.permissions < 1:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'detail': "Unauthorized"})

    date_today = ptime.now(tz).add(months=-3)
    date_start = ptime.parse(str(date_today))

    try:
        async with httpx.AsyncClient() as client:
            responses = await client.get(f"https://api.github.com/repos/oso1248/db_material/issues?state={state}&labels={label}&since={date_start}", headers={'Authorization': f'Bearer {token}'})

        responses = responses.json()

        if len(responses) == 0:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

        for response in responses:
            response['owner'] = response['assignee']['login']
            response['label'] = response['labels'][0]['name']

        return responses

    except Exception as error:
        logger.error(f'{error}')
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
