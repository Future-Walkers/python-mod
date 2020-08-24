from wisbec.console import shell
from wisbec import system


def calc_hash_name_by_openssl_x509(cacert_path):
    args = ['openssl', 'x509', '-subject_hash_old', '-in', cacert_path]
    code, out, err = shell.exec_cmd(args)
    if code != 0:
        return None
    return '{}.0'.format(out.split(system.get_newline_ch())[0])
