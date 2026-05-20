<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入联系人信息"
                show-search
                label="联系人管理"
                @search="handleQuery">
            <template v-slot:ft>
                <el-button type="primary" @click="CreateAdd" v-hasPermi="['erp:partner:add']">添加新联系人</el-button>
            </template>
            <template v-slot:bottom-ft>

            </template>
        </header-view>

        <el-row :gutter="20" style="margin: 15px 0px">
            <el-col :span="24">
                <el-table
                        v-loading="loading"
                        :data="partnerList"
                        border
                        stripe
                        style="width: 100%;"
                        show-header
                        highlight-current-row
                        @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="55" align="center"/>
                    <!-- <el-table-column label="关注" align="center" fixed  width="65">
                        <template #default="scope">
                            <svg-icon icon-class="el-icon-star-off" site="18"/>
                        </template>
                    </el-table-column> -->
                    <el-table-column label="公司名称" align="left" fixed prop="partnerName" width="250">
                        <template #default="scope">
                            <a style="color: #0052cc !important; text-overflow:ellipsis; white-space: nowrap; overflow:hidden; width:100%;"
                               @click="OpenDetail(scope.row)" :title="scope.row.partnerName">{{ scope.row.partnerName
                                }}</a>
                        </template>
                    </el-table-column>
                    <el-table-column label="首要联系人" align="center" prop="invoice_tel" width="120"/>
                    <el-table-column label="手机" align="center" prop="invoice_tel" width="120"/>
                    <el-table-column label="电话" align="center" prop="invoice_tel" width="120"/>
                    <el-table-column label="邮箱" align="center" prop="isSupplier" width="160"/>

                    <el-table-column label="客户标签" align="center" prop="partnerTag" width="160"/>
                    <el-table-column label="综合评分" align="center" prop="partnerScope" width="160">
                        <template #default="scope">
                            <el-rate v-model="scope.row.partnerScope" :colors="colors" disabled/>
                        </template>
                    </el-table-column>
                    <el-table-column label="网站" align="center" prop="website" width="200"/>
                    <el-table-column label="备注" align="center" prop="remark" width="200"/>
                    <el-table-column label="状态" align="center" prop="status" width="120">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.status">已成交</el-tag>
                            <el-tag type="info" v-else>未成交</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="创建时间" align="center" prop="createTime" width="160"/>
                    <el-table-column label="创建人" align="center" prop="isCustomer" width="120"/>
                </el-table>
                <div class="p-contianer">
                    <pagination
                            :page-sizes="[14, 20, 30, 40, 50, 100]"
                            v-show="total > 0"
                            :total="total"
                            v-model:page="queryParams.pageNum"
                            v-model:limit="queryParams.pageSize"
                            @pagination="getCustomerList"/>
                </div>
            </el-col>
        </el-row>

        <!--详情中心-->
        <DetailViews v-model="isDetailOpen" :customerData="customerData" @closeHandle="DetailClose"></DetailViews>

        <!--创建中心-->
        <CreateViews :title="'新建客户'" titleShow v-model="isOpen" @closeHandle="CreateClose"></CreateViews>
    </div>
</template>

<script setup name="contacts">
    import HeaderView from "@/components/HeaderView";
    import DetailViews from "./components/detail.vue";
    import CreateViews from "./components/create.vue";

    const {proxy} = getCurrentInstance();
    const {sys_customer_source, sys_company_nature, sys_company_industry, sys_company_type} = proxy.useDict("sys_customer_source", "sys_company_nature", "sys_company_industry", "sys_company_type");

    import {
        listContacts,
        getContacts,
        delContacts,
        addContacts,
        updateContacts,
    } from "@/api/erp/contacts";

    const isDetailOpen = ref(false)
    const isOpen = ref(false)
    const loading = ref(false)
    const total = ref(0);
    const partnerList = ref([]);
    const customerData = ref({});
    const colors = ref(['#99A9BF', '#F7BA2A', '#FF9900'])

    const data = reactive({
        queryParams: {
            pageNum: 1,
            pageSize: 14,
            partnerName: null,
            partnerKey: null,
            partnerEntity: null,
            isSupplier: null,
            isCustomer: null,
            status: null,
            isAvailable: null
        },
    });

    const {queryParams} = toRefs(data);

    /**查询客户来源 */
    function getCustomerFrom(res) {
        const scs = sys_customer_source.value.filter(source => {
            if (source.value == res) {
                return source
            }
        })
        return scs[0].label
    }

    /**查询公司性质 */
    function getCustomerNature(res) {
        const scn = sys_company_nature.value.filter(nature => {
            if (nature.value == res) {
                return nature
            }
        })
        return scn[0].label
    }

    /**查询公司类型 */
    function getCustomerType(res) {
        const scn = sys_company_type.value.filter(type => {
            if (type.value == res) {
                return type
            }
        })
        return scn[0].label
    }

    /**查询客户行业 */
    function getCustomerIndustry(res) {
        const sci = sys_company_industry.value.filter(industry => {
            if (industry.value == res) {
                return industry
            }
        })
        return sci[0].label
    }

    /** 查询商业伙伴列表 */
    function getCustomerList() {
        loading.value = true;
        listContacts(queryParams.value).then((response) => {
            partnerList.value = response.rows;
            total.value = response.total;
            loading.value = false;
        });
    }

    // 多选框选中数据
    function handleSelectionChange(selection) {
        ids.value = selection.map((item) => item.id);
        single.value = selection.length != 1;
        multiple.value = !selection.length;
    }

    /** 搜索按钮操作 */
    function handleQuery(res) {
        data.queryParams.pageNum = 1
        data.queryParams.pageSize = 14
        data.queryParams.partnerName = res
        getCustomerList()
    }

    /** 添加按钮操作 */
    function CreateAdd() {
        isOpen.value = true
    }

    /**添加关闭返回值 */
    function CreateClose(res) {
        isOpen.value = res
    }

    /**打开详情 */
    function OpenDetail(res) {
        customerData.value = res
        isDetailOpen.value = true
    }

    /**详情关闭返回值 */
    function DetailClose(res) {
        isDetailOpen.value = res
    }

    onMounted(() => {
        getCustomerList()
    })
</script>