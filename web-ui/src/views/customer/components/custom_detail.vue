<template>
    <el-drawer class="drawerview" v-model="drawerdef"
        size="60%"
        :close-on-click-modal="false"
        :show-close="false"
        direction="rtl"
        :modal="false"
        :before-close="handleClose">
        <template v-if="titleShow" #header>
            <el-row :gutter="24">
                <el-col :span="12">
                    <h4>{{ customer_info.customerName }}</h4>
                </el-col>
                <el-col :span="12" style="text-align: right;">
                    <el-button type="primary" v-hasPermi="['erp:partner:add']" class="edit-btn" @click="handleEdit">编辑</el-button>

                    <el-dropdown
                            v-if="detailMoreHandle.length > 0"
                            trigger="click"
                            style="margin-left: 5px; margin-right: 10px;"
                            @command="headerMoreHandleClick">
                        <el-button color="#f1f1f1">
                            <el-icon size="20">
                                <more-filled/>
                            </el-icon>
                        </el-button>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item
                                        v-for="(item, index) in detailMoreHandle"
                                        :key="index"
                                        :icon="item.icon"
                                        :command="item.type">{{ item.name }}
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </el-col>
            </el-row>
        </template>
        <template #default>
            <el-button
                    v-if="showClose"
                    class="close-btn"
                    type="primary"
                    icon="DArrowRight"
                    @click="handleClose"/>
            <div class="help">
                <div class="detail-base">
                    <div class="base-item">
                        <div class="base-title">手机:</div>
                        <div class="base-value text-one-line">{{customer_info.contactNumber }}</div>
                    </div>
                    <div class="base-item">
                        <div class="base-title">负责人:</div>
                        <div class="base-value text-one-line">{{ customer_info.contactPerson }}</div>
                    </div>
                    <div class="base-item">
                        <div class="base-title">Email:</div>
                        <div class="base-value text-one-line">{{ customer_info.contactEmail }}</div>
                    </div>
                    <div class="base-item">
                        <div class="base-title">联系人地址:</div>
                        <div class="base-value text-one-line">{{ customer_info.contactAddress }}</div>
                    </div>
                    <div class="base-item">
                        <div class="base-title">创建时间:</div>
                        <div class="base-value text-one-line">{{ customer_info.createTime }}</div>
                    </div>
                </div>
         
                <div class="detail-create-bar">
                    <el-button type="info" :icon="Edit" class="create-but" plain>创建运单</el-button>
                    <el-button type="info" :icon="Message" class="create-but" plain>发送邮件</el-button>
                    <el-button type="info" :icon="Comment" class="create-but" plain>发送短信</el-button>
                    <el-button type="info" :icon="Guide" class="create-but" plain>创建联系人</el-button>
                </div>
                <el-row :gutter="24" class="customerTabs" style="margin: 20px 0px 0px 0px; box-sizing: border-box; flex-wrap: wrap; justify-content: space-between;">
                    <el-col :span="24" style="padding: 0px;">
                        <el-tabs v-model="activeName" @tab-click="handleTabs">
                            <el-tab-pane label="详细资料" name="detail">
                                <template v-if="isEdit">
                                    <el-form ref="partnerRef" :model="form" :rules="rules" labelPosition="top" :inline="false">
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-form-item label="客户名称">
                                                    <el-input v-model="form.customerName"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-form-item label="社会信用代码">
                                                    <el-input v-model="form.customerTaxId"></el-input>
                                                </el-form-item>
                                            </el-col>
                                        </el-row>
                                    </el-form>
                                </template>
                                <template v-else>
                                    <el-form ref="partnerRef" disabled :model="form" :rules="rules" labelPosition="top" :inline="false">
                                        <el-row :gutter="24">
                                            <el-col :span="12">
                                                <el-form-item label="客户名称">
                                                    <el-input v-model="form.customerName"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="12">
                                                <el-form-item label="客户名称">
                                                    <el-input v-model="form.customerTaxId"></el-input>
                                                </el-form-item>
                                            </el-col>
                                        </el-row>
                                    </el-form>

                                </template>

                            </el-tab-pane>
                            <el-tab-pane label="工商信息" name="industrial">工商信息</el-tab-pane>
                            <el-tab-pane label="操作记录" name="record">
111
                                <!-- <el-steps direction="vertical" :active="1" v-if="customer_record.length > 0">
                                    <el-step v-for="(item, index) in customer_record" aria-label="11"  :key="index" :title="item.operationName" description="这是一段很长很长很长的描述性文字"></el-step>
                                    <el-step title="步骤 2"></el-step>
                                    <el-step title="步骤 3" description="这是一段很长很长很长的描述性文字"></el-step>
                                </el-steps> -->

                            </el-tab-pane>
                        </el-tabs>
                    </el-col>
                </el-row>
            </div>
        </template>
    </el-drawer>
</template>

<script setup name="DetailViews">
    import {onMounted, reactive, toRefs} from 'vue'
    import {
        Memo,
        Money,
        Edit,
        Message,
        Comment,
        Guide,
    } from '@element-plus/icons-vue'

    import {
        getInfo
    } from "@/api/customer/info";

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
        customerData: {
            type: Object,
            default: ""
        },
        titleShow: {
            type: Boolean,
            default: true
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

    const {title, customerData, titleShow, footerShow, showClose} = toRefs(props)
    const isEdit = ref(false)


    const form = reactive({
        customerName: '', //'客户名称',
        customerTaxId: '', // '社会信用代码',
        depositBank: '', // '开户银行',
        bankAccount: '', //'银行账号',
        contactPerson: '', /// '联系人',
        contactNumber: '', // '联系电话',
        contactEmail: '', // '联系邮箱',
        contactAddress: '', // '企业地址',
        settlementMode: '', // '结算方式',
        useStatus: '', //'使用状态',
        remark: '', // '备注',
        dataRealm: '', //'数据权限',
        parkCode: '', //'园区代码',
    })

    const detailMoreHandle = ref([
        {name: "打印", icon: ""},
        {name: "转移", icon: ""},
        {name: "锁定", icon: ""},
        {name: "解锁", icon: ""},
        {name: "删除", icon: ""},
    ])
    const customer_info = ref(
        {
            "customerId": 284407,
        }
    )
    const rules = reactive({
        customer_name: [
            {required: true, message: "客户名称不能为空", trigger: "blur"},
            {min: 6, max: 250, message: '长度在 6 到 60 个字符', trigger: 'blur'}

        ]
    })

    const customer_record = ref([])

    const activeName = ref("detail")

    const drawerdef = computed({
        get: () => props.value,
        set: (val) => {
            emit('update:value', val)
        }
    });

    const emit = defineEmits(['update:value', 'closeHandle']);

    const handleClose = (res) => {
        console.log(res)
        emit('closeHandle', false);
    }

    function headerMoreHandleClick(res) {
        console.log(res)
    }

    function handleTabs(res) {
        console.log(res)
        activeName.value = res
    }

    function handleEdit(res) {
        isEdit.value = true
        // console.log(res)
    }

    const customerItem = computed({
        get: () => props.customerData,
        set: (val) => {
            emit('update:customerData', val)
        }
    });

    function getDetailCustomerById() {
        if (!props.customerData.customerId) {
            return
        }
        
        getInfo(props.customerData.customerId).then(response => {
            customer_info.value = response.data;
            form.value = response.data
            console.log(form.value)
        });
    }


    watch(() => props.customerData, (newVal) => {
        console.log('customerData变化:', newVal);
        getDetailCustomerById()
        
    }, { deep: true });
</script>

<style lang="scss" scoped>
    $--but-color-primary: #0858a8;
    .drawerview {
        overflow: initial;
        h4 {
            display: flex;
            overflow: hidden;
            font-size: 24px;
            line-height: 32px;
            font-weight: 700;
            margin: 0px;
            color: #172b4d;
            text-overflow: ellipsis;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
        }
    }

    .el-drawer {
        overflow: initial;

        &__header {
            padding: 26px;
        }
    }

    .detail-create-bar {
        margin: 10px 0px;
        overflow-x: auto;
        white-space: nowrap;
    }

    .close-btn {
        position: absolute;
        top: 160px;
        left: -40px;
        z-index: 999999;
        padding: 6px;
        border-radius: 4px;
        background-color: $--but-color-primary;
        border-color: $--but-color-primary;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
        height: 40px;
        font-size: 26px;
        box-shadow: -2px 4px 6px 0px rgba(0, 0, 0, 0.3);

        i {
            margin-right: 0;
            font-size: 36px;
            font-weight: 700;
        }
    }

    .detail-head-base {
        padding: 16px;
        background-color: #f4f5f7;
        border-radius: 3px;
        font-size: 14px;
        line-height: 24px;
    }

    .detail-head-base .base-title {
        color: #6b778c;
    }

    .detail-head-base .base-value {
        min-height: 14px;
        margin-top: 8px;
    }
    .detail-base {
        margin-top: 10px;
    }

    .detail-base .base-title {
        color: #6b778c;
        margin-right: 8px;
    }

    .detail-base .base-value {
        align-items: center;
        display: inline-flex;
        color: #172b4d;
    }

    .text-one-line {
        white-space: nowrap;
    }

    .edit-btn {
        background-color: $--but-color-primary;
        border-color: $--but-color-primary;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;

        i {
            margin-right: 0;
            font-size: 36px;
        }
    }

    .create-but {
        border: 0px;
        font-size: 14px;
        color: #344563;
        line-height: 36px;
        height: 36px;
        border-radius: 2px;

        &:hover {
            background-color: #e9e9e9
        }
    }

    .customerTabs {
        font-size: 14px;
        margin-top: 20px;
    }

    .boxitem {
        font-size: 14px;
    }

    .boxitem ul {
        margin: 0px;
        padding: 0px;
        list-style: none;
    }

    .boxitem ul li {
        flex-wrap: wrap;
        line-height: 38px;
        word-break: break-word;
    }

    .detail-base {
        position: relative;
    }

    .detail-base .base-item {
        align-items: center;
        display: flex;
        min-height: 24px;
        overflow: hidden;
    }
</style>