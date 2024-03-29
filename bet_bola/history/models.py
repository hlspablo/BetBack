from django.db import models
from django.conf import settings
import utils.timezone as tzlocal

class TicketValidationHistory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    who_validated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_ticket_validations', verbose_name='Quem Validou')
    ticket = models.ForeignKey('ticket.Ticket', on_delete=models.CASCADE, verbose_name='Bilhete Validado')
    date = models.DateTimeField(verbose_name='Data da Validação')
    bet_value = models.DecimalField(max_digits=30, decimal_places=2,verbose_name='Valor Apostado')
    balance_before = models.DecimalField(max_digits=30, decimal_places=2,null=True,blank=True, verbose_name='Saldo Anterior')
    balance_after = models.DecimalField(max_digits=30, decimal_places=2,null=True, blank=True, verbose_name='Saldo Posterior')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Validação de Aposta'
        verbose_name_plural = 'Validações de Apostas'


class TicketCancelationHistory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    who_cancelled = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_canceled_tickets', on_delete=models.CASCADE, verbose_name='Quem Cancelou ?')
    ticket = models.ForeignKey('ticket.Ticket', on_delete=models.CASCADE, verbose_name='Bilhete Cancelado')
    date = models.DateTimeField(verbose_name='Data do Cancelamento')
    who_paid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_canceled_tickets_who_i_paid', verbose_name='Quem Pagou o Ticket Cancelado')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return "Cancelamento de Bilhete"

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Cancelamento de Bilhete'
        verbose_name_plural = 'Cancelamento de Bilhetes'


class CreditTransactions(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    creditor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="credit_transactions",verbose_name='Gerente')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Cambista')
    transaction_date = models.DateTimeField(verbose_name='Data da Transação', default=tzlocal.now)
    transferred_amount = models.DecimalField(max_digits=30, decimal_places=2,verbose_name='Valor Transferido')
    creditor_before_balance = models.DecimalField(max_digits=30, decimal_places=2,null=True,blank=True, verbose_name='Saldo Anterior')
    creditor_after_balance = models.DecimalField(max_digits=30, decimal_places=2,null=True,blank=True, verbose_name='Saldo Atual')
    user_before_balance = models.DecimalField(max_digits=30, decimal_places=2,null=True,blank=True, verbose_name='Saldo Anterior(Cambista)')
    user_after_balance = models.DecimalField(max_digits=30, decimal_places=2,null=True,blank=True, verbose_name='Saldo Atual(Cambista)')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return " Transf. - Gerentes"

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Transf. - Gerente'
        verbose_name_plural = 'Transf. - Gerentes'


class SellerCashierHistory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    register_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='quem prestou conta')
    tickets_registered = models.ManyToManyField('ticket.Ticket')
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE, related_name="cashiers_history", verbose_name='Cambista')
    date = models.DateTimeField(verbose_name='Data da Transação', default=tzlocal.now)
    entry = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='Entrada Total')
    comission = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='% Comissão')
    bonus_premio = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name='Bônus por Prêmio')
    out = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='Saída')
    total_out = models.DecimalField(max_digits=40, decimal_places=2,null=True, blank=True, verbose_name='Saída Total')
    profit = models.DecimalField(max_digits=30, decimal_places=2,null=True, blank=True, verbose_name='Lucro')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return "Pag. - Cambistas"

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Pag. - Cambista'
        verbose_name_plural = 'Pag. - Cambistas'


class CashierCloseSeller(models.Model):
    register_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Quem prestou conta')
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE,related_name="my_closed_cashiers", verbose_name='Cambista em questão')
    date = models.DateTimeField(verbose_name='Data da Transação', default=tzlocal.now)
    start_date = models.DateTimeField(verbose_name='Data Início')
    end_date = models.DateTimeField(verbose_name='Data Fim')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "{register_by}, {seller}, {date}, {start_date}, {end_date}"\
            .format(register_by=self.register_by, 
            seller=self.seller,
            date=self.date,
            start_date=self.start_date,
            end_date=self.end_date
        )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Fechamento - Cambista'
        verbose_name_plural = 'Fechamentos - Cambistas'

class CashierCloseManager(models.Model):
    register_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Quem prestou conta')
    manager = models.ForeignKey('user.Manager', on_delete=models.CASCADE,related_name="my_closed_cashiers", verbose_name='Gerente em questão')
    date = models.DateTimeField(verbose_name='Data da Transação', default=tzlocal.now)
    start_date = models.DateTimeField(verbose_name='Data Início')
    end_date = models.DateTimeField(verbose_name='Data Fim')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "{register_by}, {manager}, {date}, {start_date}, {end_date}"\
            .format(register_by=self.register_by, 
            manager=self.manager,
            date=self.date,
            start_date=self.start_date,
            end_date=self.end_date
        )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Fechamento - Gerente'
        verbose_name_plural = 'Fechamentos - Gerentes'

class ManagerCashierHistory(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    register_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='quem prestou conta')
    tickets_registered = models.ManyToManyField('ticket.Ticket')
    manager = models.ForeignKey('user.Manager', on_delete=models.CASCADE, related_name="cashiers_history",verbose_name='Gerente')
    date = models.DateTimeField(verbose_name='Data da Transação', default=tzlocal.now)
    entry = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='Entrada Total')
    comission = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='% Comissão')
    out = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True, verbose_name='% Comissão')
    total_out = models.DecimalField(max_digits=40, decimal_places=2,null=True, blank=True, verbose_name='Saída Total')
    profit = models.DecimalField(max_digits=30, decimal_places=2,null=True, blank=True, verbose_name='Lucro')
    store = models.ForeignKey('core.Store', verbose_name='Banca', on_delete=models.CASCADE)


    def __str__(self):
        return "Pag. - Gerentes"

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Pag. - Gerente'
        verbose_name_plural = 'Pag. - Gerentes'

