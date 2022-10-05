from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql

user  = ''

conn = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "12341234",
    db = "test"
)
curAnswer    = conn.cursor()
curScore     = conn.cursor()
curUserScore = conn.cursor()
curAnswer.execute( 'SELECT answer FROM ctfdata' )
curScore.execute( 'SELECT score FROM ctfdata' )

answerList = [ item[0] for item in curAnswer.fetchall() ]
scoreList  = [ item[0] for item in curScore.fetchall() ]
ctfdict    = {}

for answer, score in zip( answerList, scoreList ):
    ctfdict[answer] = score

def login( request ):
    request.session.flush()
    global user
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
        cur1.execute( 'SELECT id FROM tbluser' )
        cur2.execute( 'SELECT password FROM tbluser' )
        idList = [ item[0] for item in cur1.fetchall() ]
        pwList = [ item[0] for item in cur2.fetchall() ]
        userLoginData = {}

        for key, value in zip( idList, pwList ):
            userLoginData[key] = value
    

        conn.close()
        cur1.close()
        cur2.close()

        if id in userLoginData and userLoginData[id] == pw:
            message = { 'message':'Success' }
            request.session['id'] = id
            user = id
            return render( request, 'testapp/message.html', message )
            
        else:
            message = { 'message':'Failure' }
            return render( request, 'testapp/message.html', message )
            
    return render( request, 'testapp/login.html' )
        
def logout( request ):
    global score
    score = 0
    request.session.flush()
    return redirect( '/' )


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
        cur.execute( "INSERT INTO tbluser( id, password, score ) VALUES ( '{0}', '{1}', 0 )".format( id, pw ) )
        conn.commit()
        
        conn.close()
        cur.close()

    return render( request, 'testapp/signup.html' )

def ctf( request ):
    global answerList
    global ctfdict
    conn = pymysql.connect(
                host = "localhost",
                user = "root",
                password = "12341234",
                db = "test"
            )
    curScore = conn.cursor()
    curScore.execute( "SELECT score FROM tbluser WHERE id = '{0}'".format( user ) )
    score = int( curScore.fetchone()[0] )
    curScore.close()

    if request.method == 'POST':
        answer = request.POST.get( 'answer' )


        if answer in answerList:
            
            conn = pymysql.connect(
                host = "localhost",
                user = "root",
                password = "12341234",
                db = "test"
            )

            score += ctfdict[answer]
            curUpdate = conn.cursor()
            curUpdate.execute( "UPDATE tbluser SET score='{0}' WHERE id='{1}'".format( score, user ) )
            conn.commit()
            curUpdate.close()
            conn.close()

    data = { 'username':user, 'score':score }


    return render( request, 'testapp/ctf.html',  data)

def mypage( request ):
    conn = pymysql.connect(
                host = "localhost",
                user = "root",
                password = "12341234",
                db = "test"
            )

    curScore = conn.cursor()
    curScore.execute( "SELECT score FROM tbluser WHERE id = '{0}'".format( user ) )
    score = curScore.fetchone()[0]
    conn.commit()
    curScore.close()
    conn.close()

    data = { 'id':user, 'score':score }

    return render( request, 'testapp/mypage.html', data )


# Create your views here.
