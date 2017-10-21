from flaski.database import init_db
from flaski.database import db_session
from flaski.models import WikiContent

c1 = WikiContent("hoge", "hoge.gif")
db_session.add(c1)
db_session.commit()
