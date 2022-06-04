# class Comment :                          # not in use currently
#     def __init__(self,id,content) :
#         self.id = id
#         self.content = content

class Query :
    def __init__(self,id,title,comments={}) :
        self.id = id
        self.title = title
        self.comment_id_content = comments

    def update_comments(self, comments) :
        self.comment_id_content = comments

    def get_comment(self, id) :
        return self.comment_id_content[id]

    def get_comment(self) :
        return self.comment_id_content