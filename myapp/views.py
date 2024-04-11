from django.shortcuts import render,redirect
from myapp.models import userreg,product,cart,onlinemaster,onlinesub,feedback
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.db.models import Max,Value
from django.db.models import F
from datetime import date
import pyttsx3
# Create your views here.
def index(request):
    return render(request,"index.html")
def registeration(request):
        if request.method == "POST":
            mfn = request.POST.get('fn')
            mob = request.POST.get('num')
            em = request.POST.get('email')
            pw = request.POST.get('pswd')
            ua = userreg(fname=mfn,mobile=mob,email=em,password=pw)
            ua.save()
            return redirect("/h/")
        return render(request,"registeration.html")

def addproduct(request):
    if request.method=="POST":
        prid = request.POST.get('prid')
        prname = request.POST.get('prname')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        photo = request.FILES['file']
        ua = product(prid=prid,prname=prname,price=price,stock=stock,photo=photo)
        ua.save()
    return render(request,"adminaddproduct.html")
def listproduct(request):
    crec=product.objects.all()
    return render(request, "adminlistproduct.html",{"crec":crec})
def delprogram(request,id):
    product.objects.filter(id=id).delete()
    return redirect("/ap/")

def editproduct(request,id):
    if request.method=="POST":
        prid = request.POST.get('prid')
        prname = request.POST.get('prname')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        product.objects.filter(id=id).update(prid=prid,prname=prname,price=price,stock=stock)
        return redirect("/ap/")
    mrec=product.objects.filter(id=id)
    for j in mrec:
        mpc=j.prid
        mpn=j.prname
        f=j.photo
        p=j.price
        s=j.stock
    return render(request,"admineditproduct.html",{"mpc":mpc,"mpn":mpn,"f":f,"p":p,"s":s})



def login(request):
    if request.method=="POST":
        u =request.POST.get('un')
        p =request.POST.get('psw')
        urec=userreg.objects.filter(email=u,password=p)
        if urec.exists():
            for j in urec:
                id=j.id
                n=j.fname
                r=j.rights
            request.session['id']=id
            request.session['name']=n
            request.session['uname']=u
            request.session['psw']=p
            request.session['right']=r
            if r=="admin":
                return redirect("/sap/")
            elif r=="user":
                return redirect("/sup/")
        else:
            engine=pyttsx3.init()
            msg="invalid user"
            engine.say(msg)
            engine.runAndWait()

    return render(request,"login.html")


def showadminpage(request):
    return render(request,"adminpage.html")

def showuserpage(request):
    rec=product.objects.all()
    return render(request, "userpage.html",{"rec":rec})

def order(request,id):
    mrec=product.objects.filter(id=id)
    for j in mrec:
        fname=j.prname
        price=j.price
        qty=j.stock
        photo=j.photo
    qts=[]
    for j in range(1,qty+1):
        qts.append(j)
    if request.method=="POST":
            oq=request.POST.get('qtys')
            tot=int(oq)* price
            ca=cart(slno=0,pname=fname,rate=price,qty=oq,total=tot,userid=request.session['id'])
            ca.save()
            return redirect("/sup/")

    return render(request, "userpurchase.html",{"fname":fname,"price":price,"qts":qts,"photo":photo})


def viewcart(request):
    mrec = cart.objects.filter(userid=request.session['id'])
    tot=cart.objects.filter(userid=request.session['id']).aggregate(Sum('total'))
    amt=str(tot['total__sum'])
    request.session['total'] = amt
    return render(request, 'vieworder.html', {"mrec": mrec,"amt":amt})

def removeitem(request,id):
    cart.objects.filter(id=id).delete()
    tot = cart.objects.filter(userid=request.session['id']).aggregate(Sum('total'))
    amt = str(tot['total__sum'])
    mrec = cart.objects.filter(userid=request.session['id'])
    return render(request, 'vieworder.html', {"mrec": mrec,"amt":amt})

def payment(request):
    if request.method=="POST":
        if 'p1' in request.POST:
            amt=request.session['total']
            name=request.session['name']
            return render(request, "payment.html", {"amt": amt, "name": name})
        if 'p2' in request.POST:
            return redirect("/sup")


def userpayment(request):
    if request.method == "POST":
        v = request.POST.get("address")
        u = request.POST.get("account_number")
        amt = request.session['total']
        id = request.session['id']
        fname = request.session['name']
        max_salesno = onlinemaster.objects.aggregate(max_salesno=Coalesce(Max('salesno'), Value(0)))['max_salesno']
        bno = int(max_salesno) + 1
        sa = onlinemaster(salesno=bno, userid=id, uname=fname, shipment=v, phone='944749866', cardno=u, total=amt,
                          status='New Order')
        sa.save()
        mrec = cart.objects.filter(userid=request.session['id'])
        slno=1
        for j in mrec:
            su = onlinesub(salesno=bno, slno=slno, pname=j.pname, rate=j.rate, qty=j.qty, total=j.total)
            su.save()
            product.objects.filter(prname=j.pname).update(stock=F('stock') - j.qty)
            slno=slno+1
        cart.objects.filter(userid=id).delete()
        return redirect("/sup")


def changepassword(request):
    if request.method=="POST":
        oldpass = request.POST.get("old")
        newpass = request.POST.get("n1")
        confrmpass = request.POST.get("n2")
        u = request.session['uname']
        p = request.session['psw']
        if p==oldpass:
            if newpass == confrmpass:
                userreg.objects.filter(email=u, pswd=p).update(pswd=newpass)
                msg = "Hai "+ request.session['name'] + "  Password Changed Successfully........."

            else:
                msg = "Hai " + request.session['name'] + " Sorry  Password missmatch Try Again........"
        else:
            msg = "Hai " + request.session['name'] + "  Sorry wrong Password Try Again........."
        engine = pyttsx3.init()
        engine.say(msg)
        engine.runAndWait()
        return redirect("/h/")
    return render(request, "changepass.html")



def viewsales(request):
    mrec= onlinemaster.objects.filter(userid=request.session['id'])
    return render(request, "mysales.html", {"mrec": mrec})

def viewsalessub(request,salesno):
    mrec= onlinesub.objects.filter(salesno=salesno)
    return render(request, "mysalessub.html", {"mrec": mrec})

def addfeedback(request):
    n=request.session['name']

    if request.method=="POST":
        f=request.POST.get('t2')
        p = request.POST.get('t1')
        fa=feedback(uname=n,ph=p,feed=f)
        fa.save()
        msg = "Hai " + n + " Thankyou for you valuable feedback"
        return render(request, "notfound.html", {"msg": msg})

    return render(request,"feedback.html",{"n":n})

def viewfeedback(request):
    frec=feedback.objects.all()
    return render(request,"vfeed.html",{"frec":frec})


def adminviewsales(request):
    mrec= onlinemaster.objects.filter(status='New Order')
    return render(request, "admininvoice.html", {"mrec": mrec})

def adminviewsalessub(request,salesno):
    mrec= onlinesub.objects.filter(salesno=salesno)
    return render(request, "admininvoicesub.html", {"mrec": mrec})

def invoice(request,salesno):
    onlinemaster.objects.filter(salesno=salesno).update(status='Invoice')
    return redirect("/sap/")

def adminsaleshistory(request):
    mrec= onlinemaster.objects.all()
    return render(request, "adminsales.html", {"mrec": mrec})