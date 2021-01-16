
class Record:
  def __init__(self, ir, detainee_status=None, detainee_status_date=None):
      self.ir = ir
      self.detainee_status = detainee_status
      self.detainee_status_date = detainee_status_date

  def __eq__(self, other):
    if other is None:
      return False
    return self.ir == other.ir and self.detainee_status == other.detainee_status and self.detainee_status_date == other.detainee_status_date