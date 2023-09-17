import os


class Config:
    APP_NAME = os.environ.get("APP_NAME")
    AUTH_PUBLIC_KEY_DICT: dict = {'n': 'vPxtmqdIzl50t93uQqlIPvZAPswwlbutJDXeUtdVV0cu6pUHU_cNJyX0fdKSwFd-P9fCgX-xZY4masX4mNSBXMZB41-eeLis7ub0AOBkGSe6VHWhUUyAOhPOn_7GeaeFUxI8izQ9MQPE-xGaP26ePAKDy5lPbWFizgODH9UTraldDuyLSmm3yN-HWh70Sz2cgCpVHio4GpJv8FnbyhNo9BYYJzgGR1ftgkxDL441EbIEXQR2_CHrAESDyD0hbMVYCc82gr7Nda6s12pYClggejlRk_ez_59ZE6doRaIMEVsFLDa6w_BoiRC7qChKE4RT0tKNjoPIzBAZ4FOLslIgLQ', 'e': 'AQAB', 'kty': 'RSA', 'kid': 'Fe9WOEiBUz0L11CriNsaINqnpaPwWUhdA7vSpkW5IuU'}


config = Config()
