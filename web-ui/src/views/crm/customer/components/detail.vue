<template>
    <el-drawer class="drawerview" v-model="drawerdef"
               size="80%"
               :close-on-click-modal="false"
               :show-close="false"
               direction="rtl"
               :modal="false"
               :before-close="handleClose">
        <template v-show="titleShow" #header>
            <el-row :gutter="24">
                <el-col :span="12">
                    <h4>{{ customerData.partnerName }}</h4>
                </el-col>
                <el-col :span="12" style="text-align: right;">
                    <el-button type="primary" v-hasPermi="['erp:partner:add']" class="edit-btn">编辑</el-button>

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
                <div class="detail-create-bar">
                    <el-button type="info" :icon="Edit" class="create-but" plain>创建任务</el-button>
                    <el-button type="info" :icon="Message" class="create-but" plain>发送邮件</el-button>
                    <el-button type="info" :icon="Comment" class="create-but" plain>发送短信</el-button>
                    <el-button type="info" :icon="Guide" class="create-but" plain>创建联系人</el-button>
                    <el-button type="info" :icon="Money" class="create-but" plain>创建商机</el-button>
                    <el-button type="info" :icon="Memo" class="create-but" plain>创建报价单</el-button>
                </div>
                <el-row :gutter="20" class="detail-head-base" style="margin: 0px;">
                    <el-col :span="5">
                        <div class="base-title">客户级别</div>
                        <div class="base-value">{{customerData.partnerType}}</div>
                    </el-col>
                    <el-col :span="5">
                        <div class="base-title">成交状态</div>
                        <div class="base-value">{{customerData.status}}</div>
                    </el-col>
                    <el-col :span="5">
                        <div class="base-title">负责人</div>
                        <div class="base-value">admin</div>
                    </el-col>
                    <el-col :span="5">
                        <div class="base-title">首要联系人</div>
                        <div class="base-value">A</div>
                    </el-col>
                </el-row>
                <el-row :gutter="24" class="customerTabs"
                        style="margin: 20px 0px 0px 0px; box-sizing: border-box; flex-wrap: wrap; justify-content: space-between;">
                    <el-col :span="18" style="padding: 0px;">
                        <el-tabs v-model="activeName" @tab-click="handleClick">
                            <el-tab-pane label="活动" name="activity">活动</el-tab-pane>
                            <el-tab-pane label="详细资料" name="detail">详细资料</el-tab-pane>
                            <el-tab-pane label="短信" name="message">短信</el-tab-pane>
                            <el-tab-pane label="工商信息" name="industrial">工商信息</el-tab-pane>
                            <el-tab-pane label="客户关系" name="relation">客户关系</el-tab-pane>
                            <el-tab-pane label="联系人" name="contacts">联系人</el-tab-pane>
                            <el-tab-pane label="邮件" name="email">邮件</el-tab-pane>
                            <el-tab-pane label="发票" name="invoice">发票</el-tab-pane>
                            <el-tab-pane label="任务" name="task">任务</el-tab-pane>
                            <el-tab-pane label="附件" name="appendix">附件</el-tab-pane>
                            <el-tab-pane label="操作记录" name="record">操作记录</el-tab-pane>
                            <el-tab-pane label="报价单" name="quotation">报价单</el-tab-pane>
                        </el-tabs>
                    </el-col>
                    <el-col :span="5" style="padding: 0px;">
                        <el-card class="box-card">
                            <template #header>
                                <span><b>客户摘要</b></span>
                            </template>
                            <div class="boxitem">
                                <ul>
                                    <li><span>跟进次数:</span> 11次</li>
                                    <li><span>未跟进时长:</span> 11天</li>
                                    <li><span>商机数量:</span> 11</li>
                                    <li><span>商机总额:</span> 11元</li>
                                    <li><span>成交次数:</span> 11次</li>
                                    <li><span>成交总额:</span> 11元</li>
                                    <li><span>回款总额:</span> 11元</li>
                                    <li><span>未回款总额:</span> 11元</li>
                                    <li><span>开票总额:</span> 11元</li>
                                </ul>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </template>
        <template v-if="footerShow" #footer>
            <div class="dialog-footer">
                <el-button type="primary">
                    确认提交
                </el-button>
                <el-button @click="handleClose">取消</el-button>
            </div>
        </template>
    </el-drawer>
</template>

<script setup name="DetailViews">
    import {toRefs} from 'vue'
    import {
        Memo,
        Money,
        Edit,
        Message,
        Comment,
        Guide,
    } from '@element-plus/icons-vue'

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

    const detailMoreHandle = ref([
        {name: "打印", icon: ""},
        {name: "转移", icon: ""},
        {name: "放入公海", icon: ""},
        {name: "锁定", icon: ""},
        {name: "解锁", icon: ""},
        {name: "删除", icon: ""},
    ])

    const activeName = ref("activity")

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

    function handleClick(res) {
        console.log(res)
    }


</script>

<style lang="scss" scoped>
    $--but-color-primary: #0858a8;
    .drawerview {
        overflow: initial;

        h4 {
            display: flex;
            overflow: hidden;
            font-size: 24px;
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
    }

    .detail-head-base .base-title {
        color: #6b778c;
    }

    .detail-head-base .base-value {
        min-height: 14px;
        margin-top: 8px;
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

</style>