from app.extensions import db
from .model import BaseModel
from datetime import datetime

class Payment(BaseModel):
    __tablename__ = "payments"
    
    # 訂單資訊
    merchant_trade_no = db.Column(db.String(20), unique=True, nullable=False, index=True)  # 商店訂單編號
    ecpay_trade_no = db.Column(db.String(20), unique=True, nullable=True)  # 綠界交易編號
    
    # 金額資訊
    total_amount = db.Column(db.Numeric(10, 0), nullable=False)  # 交易金額
    payment_type = db.Column(db.String(20), default='aio')  # 付款類型
    
    # 狀態資訊
    payment_status = db.Column(db.String(20), default='pending', nullable=False)  # pending, paid, failed, refunded
    payment_date = db.Column(db.DateTime, nullable=True)  # 付款完成時間
    
    # 關聯資訊
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', name="fk_payments_teacher_id"), nullable=True)  # 老師ID
    
    # 商品資訊
    item_name = db.Column(db.String(200), nullable=False)  # 商品名稱
    trade_desc = db.Column(db.String(200), default='尊貴藍勾勾')  # 交易描述
    
    # 付款方法資訊
    payment_method = db.Column(db.String(50), nullable=True)  # 實際付款方式 (Credit_CreditCard, ATM, CVS...)
    payment_type_charge_fee = db.Column(db.Numeric(10, 0), default=0)  # 付款手續費
    
    # 綠界回傳資訊
    rtn_code = db.Column(db.String(10), nullable=True)  # 回傳碼
    rtn_msg = db.Column(db.String(200), nullable=True)  # 回傳訊息
    auth_code = db.Column(db.String(20), nullable=True)  # 授權碼
    
    # 信用卡資訊（如果是信用卡付款）
    card4no = db.Column(db.String(4), nullable=True)  # 信用卡後四碼
    card6no = db.Column(db.String(6), nullable=True)  # 信用卡前六碼
    
    # 其他綠界欄位
    gwsr = db.Column(db.String(20), nullable=True)  # 綠界交易序號
    process_date = db.Column(db.DateTime, nullable=True)  # 處理時間
    simulate_paid = db.Column(db.String(1), default='0')  # 是否為模擬付款
    
    # 客製化欄位
    custom_field1 = db.Column(db.String(50), nullable=True)  # 自訂欄位1
    custom_field2 = db.Column(db.String(50), nullable=True)  # 自訂欄位2
    custom_field3 = db.Column(db.String(50), nullable=True)  # 自訂欄位3
    custom_field4 = db.Column(db.String(50), nullable=True)  # 自訂欄位4
    
    # 關聯關係
    teacher = db.relationship("Teacher", backref="payments", lazy=True)
    
    def __repr__(self):
        return f"<Payment {self.merchant_trade_no}: {self.payment_status}>"
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'merchant_trade_no': self.merchant_trade_no,
            'ecpay_trade_no': self.ecpay_trade_no,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'teacher_id': self.teacher_id,
            'item_name': self.item_name,
            'trade_desc': self.trade_desc,
            'payment_method': self.payment_method,
            'rtn_code': self.rtn_code,
            'rtn_msg': self.rtn_msg,
            'auth_code': self.auth_code,
            'card4no': self.card4no,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def create_payment_record(cls, merchant_trade_no, total_amount, item_name, **kwargs):
        """建立付款記錄的便利方法"""
        payment = cls(
            merchant_trade_no=merchant_trade_no,
            total_amount=total_amount,
            item_name=item_name,
            payment_status='pending',
            **kwargs
        )
        db.session.add(payment)
        db.session.commit()
        return payment
    
    def update_payment_result(self, payment_data):
        """更新付款結果"""
        self.ecpay_trade_no = payment_data.get('TradeNo')
        self.rtn_code = payment_data.get('RtnCode')
        self.rtn_msg = payment_data.get('RtnMsg', '')
        self.payment_method = payment_data.get('PaymentType')
        self.payment_type_charge_fee = payment_data.get('PaymentTypeChargeFee', 0)
        self.auth_code = payment_data.get('auth_code')
        self.card4no = payment_data.get('card4no')
        self.card6no = payment_data.get('card6no')
        self.gwsr = payment_data.get('gwsr')
        self.simulate_paid = payment_data.get('SimulatePaid', '0')
        
        # 更新處理時間
        if payment_data.get('process_date'):
            try:
                self.process_date = datetime.strptime(
                    payment_data['process_date'], 
                    '%Y/%m/%d %H:%M:%S'
                )
            except:
                self.process_date = datetime.now()
        
        # 根據回傳碼設定狀態
        if self.rtn_code == '1':
            self.payment_status = 'paid'
            self.payment_date = datetime.now()
        else:
            self.payment_status = 'failed'
            
        db.session.commit()
