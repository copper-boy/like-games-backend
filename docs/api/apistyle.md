# Documentation

## API Introduction

### API Style
API writing style in my small 
application includes: `ease of use`, 
`simple scaling` (new logic is added by
extension, not by modification), 
`logic separation`.

#### Ease Of Use
The ease of use implies not only the 
simplification of writing code, but also 
its use by the client.

Best practice:
```python
# You need to design the API endpoint
"""
This module provides access to the `x` API.
TODO: implement the `x` API logic. Import from utils/x.py async function get_x_api_result
"""
from fastapi import APIRouter
from starlette import status

from utils.x import get_x_api_result

router = APIRouter()


@router.get(
    path="/api.x/some/get",
    response_description="The `x` API result",
    status_code=status.HTTP_200_OK,
)
async def get_some() -> dict:
    to_return: dict = await get_x_api_result()

    return to_return
```
