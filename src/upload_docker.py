import os
from pygit2 import Repository

root = os.path.dirname(__file__)
repo = Repository(os.path.join(root, '..'))
version = repo.head.shorthand

def main(version: str):
    for r, _, file in os.walk(root):
        if 'Dockerfile' in file:
            work_dir = os.path.basename(r)
            image_name = f'docker.peidan.me/wxr20/hipster-shop/{work_dir}:{version}'
            os.system(f'docker build -t {image_name} {r}')
            os.system(f'docker pull {image_name}')
    print(f'上传 {version} 版本的docker完毕')

if __name__ == '__main__':
    main(version)