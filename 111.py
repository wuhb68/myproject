class ErrorDict(dict):
    def __str__(self):
        return '哈哈哈'

    def as_p(self):
        for k, v in self.items():
            tpl = f"<p>{k}</p>"
            print(tpl)

    def as_ul(self):
        for k, v in self.items():
            tpl = f"<li>{k}{v}</li>"
            print(tpl)


obj = ErrorDict({'kq':122})
# obj['k1'] = [123, 456]
# obj['k2'] = [666, 999]
print(obj)
obj.as_p()
obj.as_ul()

# from django_redis import get_redis_connection
#
# conn = get_redis_connection("default")
# conn.set("xx", "123123")
# conn.get("xx")
