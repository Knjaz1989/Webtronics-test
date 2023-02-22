


def decode_token(token: str) -> dict | str:
    try:
        data = jwt.decode(token, config.SECRET, algorithms=[config.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong token or it has expired",
        )
    return data
