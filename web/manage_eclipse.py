#!/usr/bin/env python
import os
import manage

if __name__ == "__main__":
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("SECRET_KEY", "1234f_do%yrca+%l$i+xr^^fh4212*#fd!zz45me6r64-icbi(")
    os.environ.setdefault("DB_ENGINE", "django.db.backends.sqlite3")
    os.environ.setdefault("DB_NAME", os.path.join(os.path.dirname(os.path.abspath(__file__)), "db.sqlite3"))
    os.environ.setdefault("DB_USER", "")
    os.environ.setdefault("DB_PASS", "")
    os.environ.setdefault("DB_SERVICE", "")
    os.environ.setdefault("DB_PORT", "")

    manage.main()
