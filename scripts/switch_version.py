import os
import sys

root = os.path.join(os.path.dirname(__file__), '..', 'src')

def get_services():
    res = []
    for r, _, file in os.walk(root):
        if 'Dockerfile' in file:
            work_dir = os.path.basename(r)
            res.append(work_dir)
    return res

def switch_version(version: str):
    services = get_services()
    for svc in services:
        os.system(f'kubectl set image deployment/{svc} server=docker.peidan.me/wxr20/hipster-shop/{svc}:{version}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('⚠️  请提供版本名称')
    else:
        switch_version(sys.argv[1])