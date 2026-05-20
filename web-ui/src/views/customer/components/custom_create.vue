<template>
    <el-dialog class="drawerview" :visible.sync="drawerdef"
               size="80%"
               :close-on-click-modal="false"
               :show-close="false"
               :modal="true"
               :lock-scroll="true"
               :before-close="handleClose"
               append-to-body>
        <template v-if="titleShow" #header>
            <h4 style="margin: 0px; font-size: 20px; font-weight: 600;">{{ title }}</h4>
        </template>
        <div class="section-header">
            <span class="lineicon"></span>
            <span class="title">基础信息</span>
        </div>
        <!-- <el-form ref="partnerRef" :model="form" :rules="rules" labelPosition="top" :inline="false">
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="公司名称" prop="customerName" label-suffix="搜索工商信息">
                        <el-input v-model="form.customerName" placeholder="请输入公司名称">
                            <template #suffix>
                                <span style="position: absolute; top: -34px; right: 2px;">
                                    工商信息
                                </span>
                                <el-button class="subut" style="margin-left: -10px;" icon="search" @click="queryCustomer"></el-button>
                            </template>
                        </el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="公司法人" prop="corporation">
                        <el-input v-model="form.corporation" placeholder="请输入公司法人"/>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="税号" prop="tax_no">
                        <el-input v-model="form.taxNo" placeholder="请输入公司税号"/>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="SN编号" prop="identifysn">
                        <el-input v-model="form.identifysn" placeholder="请输入公司唯一SN编号"/>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="客户来源" prop="source">
                        <el-select v-model="form.source" placeholder="请选择客户来源" style="width: 100%;">
                            <el-option
                                    v-for="dict in sys_customer_source"
                                    :key="dict.value"
                                    :label="dict.label"
                                    :value="dict.value"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="公司性质" prop="nature">
                        <el-select v-model="form.nature" placeholder="请选择公司性质" style="width: 100%;">
                            <el-option
                                    v-for="dict in sys_company_nature"
                                    :key="dict.value"
                                    :label="dict.label"
                                    :value="dict.value"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="公司行业" prop="industry">
                        <el-select v-model="form.industry" placeholder="请选择公司行业" style="width: 100%;">
                            <el-option
                                    v-for="dict in sys_company_industry"
                                    :key="dict.value"
                                    :label="dict.label"
                                    :value="dict.value"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="公司类型" prop="types">
                        <el-select v-model="form.types" placeholder="请选择公司类型" style="width: 100%;">
                            <el-option
                                    v-for="dict in sys_company_type"
                                    :key="dict.value"
                                    :label="dict.label"
                                    :value="dict.value"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="注册资金" prop="registerCapital">
                        <el-input v-model="form.registerCapital" placeholder="请输入注册资金"/>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="标签" prop="tags">
                        <el-input v-model="form.tags" placeholder="请输入标签"/>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="公司是" prop="is_supplier" class="customerCheckbox">
                        <el-checkbox v-model="form.isSupplier">供应商</el-checkbox>
                        <el-checkbox v-model="form.isCustomer">客户</el-checkbox>
                    </el-form-item>
                </el-col>
            </el-row>
            <div class="section-header">
                <span class="lineicon"></span>
                <span class="title">开票信息</span>
            </div>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="开户行" prop="opening_bank">
                        <el-input v-model="form.openingBank" placeholder="请输入公司开户行"/>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="银行账号" prop="bank_num">
                        <el-input v-model="form.bankNum" placeholder="请输入公司银行账号"/>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="开票电话" prop="invoice_tel">
                        <el-input v-model="form.invoiceTel" placeholder="请输入公司开票电话"/>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="联行号" prop="interbank_num">
                        <el-input v-model="form.interbankNum" placeholder="请输入公司联行号"/>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="24">
                    <el-form-item label="开票地址" prop="invoice_address">
                        <el-input v-model="form.invoiceAddress" placeholder="请输入公司开票地址"/>
                    </el-form-item>
                </el-col>
            </el-row>

            <div class="section-header">
                <span class="lineicon"></span>
                <span class="title">地区信息</span>
            </div>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between; margin:0px;">
                <el-col :span="4" style="padding: 0px;">
                    <el-select v-model="form.provinceId" placeholder="请选择省份" style="width: 100%;">
                        <el-option
                                v-for="item in provinceList"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="4" style="padding: 0px;">
                    <el-select v-model="form.cityId" placeholder="请选择市" style="width: 100%;">
                        <el-option
                                v-for="item in cityList"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="4" style="padding: 0px;">
                    <el-select v-model="form.areaId" placeholder="请选择地区/县" style="width: 100%;">
                        <el-option
                                v-for="item in areaList"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="11" style="padding: 0px;">
                    <el-input v-model="form.address" placeholder="请输入详细地址"/>
                </el-col>
            </el-row>
            <div class="section-header" style="margin-top:10px;">
                <span class="lineicon"></span>
                <span class="title">证件信息</span>
            </div>
            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="11">
                    <el-form-item label="营业执照" prop="license">
                        <image-upload v-model="form.license" :limit="1"/>
                    </el-form-item>
                </el-col>
                <el-col :span="11" style="text-align: right;">
                    <el-form-item label="公司信誉" prop="ccredit">
                        <image-upload v-model="form.ccredit" :limit="1"/>
                    </el-form-item>
                </el-col>
            </el-row>

            <el-row :gutter="24"
                    style="display: flex;flex-wrap: wrap;position: relative;box-sizing: border-box;justify-content: space-between;">
                <el-col :span="24">
                    <el-form-item label="备注" prop="remark">
                        <el-input v-model="form.remark" type="textarea" placeholder="请输入备注" style="width:100%;"
                                  :rows="3"/>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form> -->
        <template #footer>
            <div class="dialog-footer">
                <el-button :loading="loading" type="primary" @click="submitForm">确 定</el-button>
                <el-button @click="handleClose">取 消</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script setup name="CreateViews">
    import {toRefs, watch} from 'vue'
    // import {listRegion} from "@/api/system/region"
    // import {getCustomerByName, getCustomer, addCustomer, updateCustomer, delCustomer} from "@/api/crm/customer"


    const {proxy} = getCurrentInstance();
    const {sys_customer_source, sys_company_nature, sys_company_industry, sys_company_type} = proxy.useDict("sys_customer_source", "sys_company_nature", "sys_company_industry", "sys_company_type");

    const props = defineProps({
        title: {
            type: String,
            default: ''
        },
        /* 是否显示检索图标 */
        value: {
            type: Boolean,
            default: false,
        },
        titleShow: {
            type: Boolean,
            default: false
        },
        footerShow: {
            type: Boolean,
            default: false
        },
        showClose: {
            type: Boolean,
            default: true
        },
    })

    const {title, titleShow, footerShow, showClose} = toRefs(props)

    const data = reactive({
        loading: false,
        form: {
            customerName: "",
            identifysn: "",
            isReceive: 1,
        },
        queryParams: {
            pageNum: 1,
            pageSize: 14,
            customerName: null,
            status: null,
        },
        regionParams: {
            pageNum: 1,
            pageSize: 100,
            parentId: 0,
            // level: 0
        },
        provinceList: [],
        cityList: [],
        areaList: [],
        rules: {
            customerName: [
                {required: true, message: "公司名称不能为空", trigger: "blur"},
                {min: 6, max: 250, message: '长度在 6 到 60 个字符', trigger: 'blur'}
            ]
        }
    });
    const {loading, form, queryParams, regionParams, provinceList, cityList, areaList, rules} = toRefs(data);


    const drawerdef = computed({
        get: () => props.value,
        set: (val) => {
            emit('update:value', val)
        }
    });

    /**监听选择省份ID值：如果有加载市 */
    watch(() => form.value.provinceId, (newVal, val) => {
        if (newVal != val) {
            regionParams.value.parentId = newVal
            regionParams.value.level = 1
            cityList.value = []
            areaList.value = []
            form.value.cityId = ""
            form.value.areaId = ""
            listRegion(regionParams.value).then(response => {
                cityList.value = response.rows
            });
        }
    }, {deep: true})

    /**监听选择市ID值：如果有加载县/区 */
    watch(() => form.value.cityId, (newVal, val) => {
        if (newVal != val) {
            regionParams.value.parentId = newVal
            regionParams.value.level = 2
            areaList.value = []
            form.value.areaId = ""
            listRegion(regionParams.value).then(response => {
                areaList.value = response.rows
            });
        }
    }, {deep: true})

    const emit = defineEmits(['update:value', 'closeHandle']);

    // 取消按钮
    const handleClose = () => {
        emit('closeHandle', false);
    }


    /** 查询地区列表 */
    function getRegionList() {
        listRegion(regionParams.value).then(response => {
            provinceList.value = response.rows
        });
    }


    function queryCustomer() {
        if (form.value.customerName == "") {
            proxy.$modal.msgError("公司名称不能为空")
            return
        }
        // getCustomerByName(form.value.customerName).then(response => {
            // console.log(response.data)
            // if (response.data.partnerName) {
            //     proxy.$modal.msgError("公司名称已存在")
            //     return
            // }
            // form.value.partnerKey = response.data.partnerKey
            // form.value.partnerEntity = response.data.partnerEntity
        // })
        console.log(form.value);
    }

    /** 提交按钮 */
    function submitForm() {
        proxy.$refs["partnerRef"].validate((valid) => {
            if (valid) {
                // 提交锁定
                data.loading = true
                if (form.value.customerId != null) {
                    // updateCustomer(form.value).then((response) => {
                    //     proxy.$modal.msgSuccess("修改成功");
                    //     open.value = false;
                    //     data.loading = false
                    //     emit('up-success', {
                    //         type: 'Partner',
                    //         data: response.data || {}
                    //     })
                    // });
                } else {
                    // addCustomer(form.value).then((response) => {
                    //     proxy.$modal.msgSuccess("新增成功");
                    //     open.value = false;
                    //     data.loading = false
                    //     emit('save-success', {
                    //         type: 'customer',
                    //         data: response.data || {}
                    //     })
                    // });
                }
            }
        });
    }

    /** 重新设置 */
    function resetForm() {
        proxy.$refs["partnerRef"].resetFields();
    }

    onMounted(() => {
        nextTick(() => {
            // 初始化主题样式
            getRegionList()
        })
    })
</script>

<style lang="scss" scoped>
    $--but-color-primary: #0858a8;

    .drawerview {
        overflow: initial;
        top: 1px;
    }

    .customerCheckbox {
        .el-checkbox__inner {
            width: 18px;
            height: 18px;
        }
    }

    .section-header {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        padding: 5px 0;
        margin-bottom: 10px;

        .lineicon {
            border-left: 4px solid rgb(35, 98, 251);
            line-height: 16px;
            height: 16px;
            border-radius: 2px;
            width: 2px;
            display: block;
        }

        .title {
            flex-shrink: 0;
            margin-left: 8px;
            font-size: 16px;
            font-weight: 600;
        }
    }

    .subut {
        margin-left: -10px;
        border: 0px;
        background: none;
        font-size: 18px;
        color: #666;
    }

    .subut:hover {
        margin-left: -8px;
        border: 0px;
        color: #000;
        background: none;
        font-size: 20px;
    }

    .subut:active {
        margin-left: -10px;
        border: 0px;
        color: #636363;
        background: none;
        font-size: 18px;
    }


    .close-btn {
        position: absolute;
        top: 160px;
        left: -40px;
        z-index: 0;
        padding: 6px;
        background-color: $--but-color-primary;
        border-color: $--but-color-primary;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
        height: 40px;
        font-size: 26px;

        i {
            margin-right: 0;
            font-size: 36px;
        }
    }
</style>
