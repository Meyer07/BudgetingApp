from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Category,Transactions,Budget
from django.db.models import Sum
from datetime import date
import json


@login_required
def dashboard(request):

    transactions = Transactions.objects.filter(user=request.user).order_by('-date')

    total_income=transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses=transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance=total_income-total_expenses

    expense_by_category = (
        transactions.filter(transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    chart_labels = json.dumps([item['category__name'] or 'Uncategorized' for item in expense_by_category])
    chart_data = json.dumps([float(item['total']) for item in expense_by_category])

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
        transaction_date=request.POST['date']
        notes=request.POST.get('notes','')

        category=Category.objects.get(id=category_id,) if category_id else None

        Transactions.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            date=transaction_date,
            notes=notes
        )
        return redirect('dashboard')
    
    categories=Category.objects.all()
    return render(request,'tracker/add_transaction.html', {'categories':categories})

@login_required
def delete_transaction(request, pk):
    transaction = Transactions.objects.get(id=pk, user=request.user)
    transaction.delete()
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def budget_goals(request):
    today=date.today()
    current_month=today.month
    current_year=today.year

    if request.method=='POST':
        category_id=request.POST.get('category')
        amount=request.POST.get('amount')
        category=Category.objects.get(id=category_id)

        Budget.objects.update_or_create(
            user=request.user,
            category=category,
            month=current_month,
            year=current_year,
            defaults={'amount':amount}
        )
        return redirect('budget_goals')
    
    categories=Category.objects.all()
    budgets=Budget.objects.filter(user=request.user, month=current_month,year=current_year)

    budget_data=[]

    for budget in budgets:
        result=Transactions.objects.filter(
            user=request.user,
            category=budget.category,
            transaction_type='expense',
            date__year=current_year,
            date__month=current_month

        ).aggregate(total=Sum('amount'))

        spent=result.get('total') or 0

        percentage=min(int((float(spent) / float(budget.amount)) * 100), 100)

        if percentage >= 90:
            color = 'danger'
        elif percentage >= 60:
            color = 'warning'
        else:
            color = 'success'

        budget_data.append({
            'category': budget.category.name,
            'limit': budget.amount,
            'spent': spent,
            'percentage': percentage,
            'color': color,
            'budget_id': budget.id,
        })
    return render(request, 'tracker/budget_goals.html', {
        'categories': categories,
        'budget_data': budget_data,
        'current_month': today.strftime('%B %Y'),
    })
@login_required
def delete_budget(request,pk):
    budget=Budget.objects.get(id=pk,user=request.user)
    budget.delete()
    return redirect('budget_goals')

