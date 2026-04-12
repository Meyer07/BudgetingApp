from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Transactions
from django.db.models import Sum


@login_required
def dashboard(request):
    transactions=Transactions.objects.all().order_by('-date')

    total_income=Transactions.objects.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses=Transactions.objects.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance=total_income-total_expenses

    expense_by_category = (
        transactions.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    chart_labels = [item['category__name'] or 'Uncategorized' for item in expense_by_category]
    chart_data = [float(item['total']) for item in expense_by_category]

    return render(request,'tracker/dashboard.html',{
        'transactions':transactions,
        'total_income':total_income,
        'total_expenses':total_expenses,
        'balance':balance,
        'chart_labels':chart_labels,
        'chart_data':chart_data
        
    })

@login_required
def add_transaction(request):
    if(request.method=='POST'):
        title=request.POST['title']
        amount=request.POST['amount']
        transaction_type=request.POST['transaction_type']
        category_id=request.POST.get('category')
        date=request.POST['date']
        notes=request.POST.get('notes','')

        category=Category.objects.get(id=category_id,) if category_id else None

        Transactions.objects.create(
            title=title,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            date=date,
            notes=notes
        )
        return redirect('dashboard')
    
    categories=Category.objects.all()
    return render(request,'tracker/add_transaction.html', {'categories':categories})

@login_required
def delete_transaction(request):
    transaction=Transactions.objects.get(id=pk)
    transaction.delete()
    return redirect('dashboard')


