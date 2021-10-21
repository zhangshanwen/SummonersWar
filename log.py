def info(*args):
    msg = " ".join(f"{i}" for i in args)
    print(f"\033[1;32;40m {msg} \033[0m")


def warning(*args):
    msg = " ".join(f"{i}" for i in args)
    print(f"\033[1;31;40m {msg} \033[0m")


def debug(*args):
    msg = " ".join(f"{i}" for i in args)
    print(f"\033[1;34;40m {msg} \033[0m")


def info_start(msg):
    info(msg + "......")


if __name__ == '__main__':
    debug("d111", "d222")
