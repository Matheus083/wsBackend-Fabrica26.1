import pymysql

# Faz o PyMySQL se passar pelo driver oficial.
pymysql.install_as_MySQLdb()

# Enganar a checagem de versão do Django.
# "Ei Django, finja que minha versão é a 2.2.1"
pymysql.version_info = (2, 2, 1, "final", 0)
