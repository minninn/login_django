from django.shortcuts import render
from django.http import HttpResponse
import pymysql

def login( request ):
    message = ''
    if request.method == 'POST':
        id = request.POST.get( 'userid' )
        pw = request.POST.get( 'password' )

        conn = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "12341234",
            db = "test"
        )
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        cur1.execute( 'SELECT id FROM testtable' )
        cur2.execute( 'SELECT password FROM testtable' )
        idList = [ item[0] for item in cur1.fetchall() ]
        pwList = [ item[0] for item in cur2.fetchall() ]
        print( idList, pwList )
        userLoginData = {}

        for key, value in zip( idList, pwList ):
            userLoginData[key] = value
        

        print( userLoginData )

        conn.close()
        cur1.close()
        cur2.close()

        if userLoginData[id] == pw:
            message = { 'message':'로그인성공' }
            print( 'success' )
        else:
            message = ''
            print( 'failure' )
    if message == '':
        return render( request, 'testapp/login.html' )
    else:
        return render( request, 'testapp/message.html', message )


def signup( request ):
    
    if request.method == 'POST':
        id = request.POST.get( 'userid' )
        pw = request.POST.get( 'password' )  

        conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "12341234",
        db = "test"
        )
        cur = conn.cursor()
        cur.execute( "INSERT INTO testtable( id, password ) VALUES ( '{0}', '{1}' )".format( id, pw ) )
        conn.commit()
        
        conn.close()
        cur.close()

    return render( request, 'testapp/signup.html' )

# Create your views here.
