def info(msg):
    print(f"\033[1;32;40m {msg} \033[0m")


def warning(msg):
    print(f"\033[1;31;40m {msg} \033[0m")


def info_start(msg):
    info(msg + "......")


if __name__ == '__main__':
    info("d111")
