import os
import asyncio
import logging
import httpx

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
)


async def login():
    """使用账号密码登陆

    Returns:
        _type_: _description_
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.nssctf.cn/api/user/login/",
            headers={"User-Agent": USER_AGENT},
            data={
                "username": os.environ["NSSCTF_USERNAME"],
                "password": os.environ["NSSCTF_PASSWORD"],
            },
        )
        cookies = dict(resp.cookies)
        cookies["token"] = resp.json()["data"]["token"]
        return cookies


async def signin(cookies):
    async with httpx.AsyncClient(cookies=cookies) as client:
        resp = await client.post(
            "https://www.nssctf.cn/api/user/clockin/",
            headers={"User-Agent": USER_AGENT},
        )
        logging.warning(resp.text)
        data = resp.json()
        return data["code"] == 200


async def coin_num(cookies):
    async with httpx.AsyncClient(cookies=cookies) as client:
        resp = await client.get(
            "https://www.nssctf.cn/api/user/info/opt/setting/",
            headers={"User-Agent": USER_AGENT},
        )
        logging.warning(resp.text)

        data = resp.json()

        if data["code"] != 200:
            return None
        return data.get("data", {}).get("coin", None)

async def main():
    cookies = await login()
    await signin(cookies)
    num = await coin_num(cookies)
    print(num)

if __name__ == "__main__":
    asyncio.run(main())
