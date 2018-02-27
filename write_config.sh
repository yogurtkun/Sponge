add_parameter() {
    echo $1 "=" \'$2\' >> code/config.py
}

rm -f code/config.py
echo 'import os' >> code/config.py

add_parameter SECRET_KEY $SECRET_KEY
add_parameter DATA_BACKEND cloudsql
add_parameter PROJECT_ID $GCLOUD_PROJECT_ID
add_parameter CLOUDSQL_USER $CLOUDSQL_USER
add_parameter CLOUDSQL_DATABASE $CLOUDSQL_DATABASE
add_parameter CLOUDSQL_PASSWORD $CLOUDSQL_PASSWORD
add_parameter CLOUDSQL_CONNECTION_NAME $CLOUDSQL_CONNECTION_NAME
add_parameter CLOUDSQL_HOST $CLOUDSQL_HOST

echo "LIVE_SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://{user}:{password}@{host}/{database}''?unix_socket=/cloudsql/{connection_name}').format(user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD, host=CLOUDSQL_HOST,database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)" >> code/config.py

echo "SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI" >> code/config.py
