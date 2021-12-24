class GetFolio:
  zero_lenght = 4
  
  def __init__(self, model):
    total = model.objects.count()
    self.total_rows = total + 1 if total > 0 else 1 

  def generate(self):
    try:
      str_zero = ''
      for cero in range((self.zero_lenght - len(str(self.total_rows)))):
        str_zero += '0'
      return '{}{}'.format(str_zero, self.total_rows)
    except:
      return '{}'.format(self.total_rows)