
import git
from git import Repo
import os
def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        Repo.clone_from(url="https://github.com/aIFzzf/MayaWorkflow.git", to_path=MayaCodePath)
        print("---  new folder...  ---")
        print( "---  OK  ---")

    else:
        g = git.cmd.Git(path)
        g.pull()
        print("---  There is this folder!  ---")

path = os.path.abspath(os.path.dirname(__file__))
MayaCodePath = path + '\\MayaCode'
mkdir(MayaCodePath)







# app = Flask(__name__)

# @app.route('/',methods=['POST'])
# def api_message2():
#     if request.headers['Content-Type'] == 'application/json':
#         if(repo.is_dirty()):
#             git.Repo.clone_from(url="https://github.com/aIFzzf/MayaWorkflow.git",to_path ="../MayaCode")
#         else:
#             repo2 = git.Repo('../MayaCode')
#             o = repo.remotes.origin
#             o.pull()
#         return 'Webhook notification received', 202
#
#
# if __name__ == '__main__':
#     app.run(debug=True)