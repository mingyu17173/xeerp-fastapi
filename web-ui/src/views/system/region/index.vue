<template>
    <div class="app-container">
        <header-view
                :ftTop="'8'"
                placeholder="请输入划区信息"
                show-search
                label="划区信息"
                @search="handleQuery">

            <template v-slot:bottom-ft>
                <RefreshView style="margin-right: 20px;" @click="resetQuery"></RefreshView>
                <ShowFilter :columns="showColumn"></ShowFilter>

            </template>
        </header-view>
        <el-row :gutter="20" style="margin: 15px 0px;">
            <el-col :span="24">
                <el-table v-loading="loading" :data="regionList" @row-click="handerRowData">
                    <el-table-column type="selection" width="55" align="center"/>
                    <!-- <el-table-column label="" align="center" prop="id" /> -->
                    <el-table-column label="划区代码" align="left" prop="code" width="140"/>
                    <el-table-column label="划区名称" align="left" prop="name"/>
                    <!-- <el-table-column label="父级" align="center" prop="parentId" /> -->
                    <el-table-column label="划区级别" align="center" prop="level" width="100"/>
                </el-table>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
    import HeaderView from '@/components/HeaderView'
    import AdvancedFilter from '@/components/AdvancedFilter'
    import ShowFilter from '@/components/showFilter'
    import RefreshView from '@/components/RefreshView'

    import {listRegion, getRegion, delRegion, addRegion, updateRegion} from "@/api/system/region";

    const {proxy} = getCurrentInstance();

    const regionList = ref([]);
    const open = ref(false);
    const loading = ref(true);
    const showSearch = ref(true);
    const ids = ref([]);
    const single = ref(true);
    const multiple = ref(true);
    const total = ref(0);
    const title = ref("");

    const data = reactive({
        form: {},
        queryParams: {
            pageNum: 1,
            pageSize: 100,

            parentId: 0,
            // level: 0
        },
        rules: {}
    });

    const showColumn = ref([
        {label: "划区代码", value: "code"},
        {label: "划区名称", value: "name"},
        {label: "划区级别", value: "level"},
    ])


    const {queryParams, form, rules} = toRefs(data);

    /** 搜索按钮操作 */
    function handleQuery(res) {
        data.queryParams.pageNum = 1;
        getList();
    }

    /** 重置按钮操作 */
    function resetQuery() {
        data.queryParams.pageNum = 1,
            data.queryParams.pageSize = 100,
            data.queryParams.parentId = 0,
            // data.queryParams.level = 0

        handleQuery();
    }

    /** 点击触发操作 */
    function handerRowData(res) {
        data.queryParams.parentId = res.id
        // data.queryParams.level = null
        getList();
    }

    /** 查询地区列表 */
    function getList() {
        loading.value = true
        listRegion(queryParams.value).then(response => {
            regionList.value = response.rows
            total.value = response.total
            loading.value = false
        });
    }

    /**数据加载... */
    onMounted(() => {
        getList();
    })


</script>