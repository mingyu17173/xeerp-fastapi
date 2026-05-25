# -*- coding: utf-8 -*-
# @Time : 2026/5/24
# @Author : fgf67@163.com<hmy>
# @FileName: partner.py
# @Software: PyCharm
# @Desc : 数据模式

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from models.partner import PartnerType, PartnerStatus

class PartnerModel(BaseModel):
    partner_id: int = Field(..., description='往来单位ID')
    partner_code: str = Field(..., description='往来单位编码')
    partner_name: str = Field(..., description='往来单位名称')
    short_name: Optional[str] = Field(None, description='简称')
    partner_type: PartnerType = Field(..., description='类型')
    status: PartnerStatus = Field(..., description='状态')
    contact_person: Optional[str] = Field(None, description='联系人')
    phone: Optional[str] = Field(None, description='联系电话')
    mobile: Optional[str] = Field(None, description='手机号码')
    email: Optional[EmailStr] = Field(None, description='邮箱')
    address: Optional[str] = Field(None, description='地址')
    province: Optional[str] = Field(None, description='省份')
    city: Optional[str] = Field(None, description='城市')
    district: Optional[str] = Field(None, description='区县')
    tax_no: Optional[str] = Field(None, description='税号')
    bank_name: Optional[str] = Field(None, description='开户银行')
    bank_account: Optional[str] = Field(None, description='银行账号')
    credit_limit: Optional[float] = Field(0, description='信用额度')
    credit_days: Optional[int] = Field(0, description='信用天数')
    remark: Optional[str] = Field(None, description='备注')
    create_time: datetime = Field(..., description='创建时间')
    update_time: Optional[datetime] = Field(None, description='更新时间')

class AddPartnerModel(BaseModel):
    partner_code: str = Field(..., description='往来单位编码')
    partner_name: str = Field(..., description='往来单位名称')
    short_name: Optional[str] = Field(None, description='简称')
    partner_type: PartnerType = Field(..., description='类型')
    contact_person: Optional[str] = Field(None, description='联系人')
    phone: Optional[str] = Field(None, description='联系电话')
    mobile: Optional[str] = Field(None, description='手机号码')
    email: Optional[EmailStr] = Field(None, description='邮箱')
    address: Optional[str] = Field(None, description='地址')
    province: Optional[str] = Field(None, description='省份')
    city: Optional[str] = Field(None, description='城市')
    district: Optional[str] = Field(None, description='区县')
    tax_no: Optional[str] = Field(None, description='税号')
    bank_name: Optional[str] = Field(None, description='开户银行')
    bank_account: Optional[str] = Field(None, description='银行账号')
    credit_limit: Optional[float] = Field(0, description='信用额度')
    credit_days: Optional[int] = Field(0, description='信用天数')
    remark: Optional[str] = Field(None, description='备注')

class EditPartnerModel(BaseModel):
    partner_id: int = Field(..., description='往来单位ID')
    partner_name: str = Field(..., description='往来单位名称')
    short_name: Optional[str] = Field(None, description='简称')
    partner_type: PartnerType = Field(..., description='类型')
    status: PartnerStatus = Field(..., description='状态')
    contact_person: Optional[str] = Field(None, description='联系人')
    phone: Optional[str] = Field(None, description='联系电话')
    mobile: Optional[str] = Field(None, description='手机号码')
    email: Optional[EmailStr] = Field(None, description='邮箱')
    address: Optional[str] = Field(None, description='地址')
    province: Optional[str] = Field(None, description='省份')
    city: Optional[str] = Field(None, description='城市')
    district: Optional[str] = Field(None, description='区县')
    tax_no: Optional[str] = Field(None, description='税号')
    bank_name: Optional[str] = Field(None, description='开户银行')
    bank_account: Optional[str] = Field(None, description='银行账号')
    credit_limit: Optional[float] = Field(0, description='信用额度')
    credit_days: Optional[int] = Field(0, description='信用天数')
    remark: Optional[str] = Field(None, description='备注')

class PartnerPageQueryModel(BaseModel):
    page_num: int = Field(1, description='页码')
    page_size: int = Field(10, description='每页数量')
    partner_code: Optional[str] = Field(None, description='往来单位编码')
    partner_name: Optional[str] = Field(None, description='往来单位名称')
    partner_type: Optional[PartnerType] = Field(None, description='类型')
    status: Optional[PartnerStatus] = Field(None, description='状态')