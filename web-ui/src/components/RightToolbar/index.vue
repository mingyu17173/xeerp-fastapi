<template>
    <div class="top-right-btn" :style="style">
        <el-row>
            <el-tooltip class="item" effect="dark" :content="showSearch ? '隐藏搜索' : '显示搜索'" placement="top"
                        v-if="search">
                <el-button circle icon="Hide" @click="toggleSearch()"/>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="高级筛选" placement="top">
                <el-button circle icon="Search" @click="screen()"/>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="刷新" placement="top">
                <el-button circle icon="Refresh" @click="refresh()"/>
            </el-tooltip>
            <el-tooltip class="item" effect="dark" content="显隐列" placement="top" v-if="columns">
                <el-button circle icon="Menu" @click="showColumn()" v-if="showColumnsType == 'transfer'"/>
                <el-dropdown trigger="click" :hide-on-click="false" style="padding-left: 12px"
                             v-if="showColumnsType == 'checkbox'">
                    <el-button circle icon="Menu"/>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <template v-for="item in columns" :key="item.key">
                                <el-dropdown-item>
                                    <el-checkbox :checked="item.visible" @change="checkboxChange($event, item.label)"
                                                 :label="item.label"/>
                                </el-dropdown-item>
                            </template>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-tooltip>
        </el-row>
        <el-dialog :title="title" v-model="open" append-to-body>
            <el-transfer
                    :titles="['显示', '隐藏']"
                    v-model="value"
                    :data="columns"
                    @change="dataChange"
            ></el-transfer>
        </el-dialog>
        <el-dialog :title="titleSc" v-model="openSc" width="750px" append-to-body :close-on-click-modal="false">
            <template class="hov">
                <el-select v-model="value" class="m-2" placeholder="Select" style="width: 25%;">
                    <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                    />
                </el-select>
                <el-select v-model="value" class="m-2" placeholder="Select" style="width: 13.3%;margin:0 10px">
                    <el-option
                            v-for="item in optionA"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                    />
                </el-select>
                <el-select v-model="value" class="m-2" placeholder="Select" style="width: 25%;">
                    <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                    />
                </el-select>
            </template>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary">确 定</el-button>
                    <el-button @click="closeModal">取 消</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    const props = defineProps({
        /* 是否显示检索条件 */
        showSearch: {
            type: Boolean,
            default: true,
        },
        /* 显隐列信息 */
        columns: {
            type: Array,
        },
        /* 是否显示检索图标 */
        search: {
            type: Boolean,
            default: true,
        },
        /* 显隐列类型（transfer穿梭框、checkbox复选框） */
        showColumnsType: {
            type: String,
            default: "checkbox",
        },
        /* 右外边距 */
        gutter: {
            type: Number,
            default: 10,
        },
    })

    const emits = defineEmits(['update:showSearch', 'queryTable']);

    // 显隐数据
    const value = ref([]);
    // 弹出层标题
    const title = ref("显示/隐藏");
    const titleSc = ref("高级筛选");
    // 是否显示弹出层
    const open = ref(false);
    const openSc = ref(false);
    const ceshi = ref('')

    const options = [
        {
            value: 'Option1',
            label: 'Option1',
        },
        {
            value: 'Option2',
            label: 'Option2',
        },
        {
            value: 'Option3',
            label: 'Option3',
        },
        {
            value: 'Option4',
            label: 'Option4',
        },
        {
            value: 'Option5',
            label: 'Option5',
        },
    ]

    const optionA = [
        {
            value: 'Option1',
            label: '等于',
        },
        {
            value: 'Option2',
            label: '不等于',
        },
        {
            value: 'Option3',
            label: '早于',
        },
        {
            value: 'Option4',
            label: '晚于',
        },
        {
            value: 'Option5',
            label: '不早于',
        },
        {
            value: 'Option5',
            label: '不晚于',
        },
        {
            value: 'Option5',
            label: '等于（时间段）',
        },
        {
            value: 'Option5',
            label: '为空',
        },
        {
            value: 'Option5',
            label: '不为空',
        },
    ]


    const style = computed(() => {
        const ret = {};
        if (props.gutter) {
            ret.marginRight = `${props.gutter / 2}px`;
        }
        return ret;
    });

    // 搜索
    function toggleSearch() {
        emits("update:showSearch", !props.showSearch);
    }

    //高级筛选
    function screen() {
        openSc.value = true;
        // emits("openSc", false);
    }

    function closeModal() {
        openSc.value = false;
    }

    // 刷新
    function refresh() {
        emits("queryTable");
    }

    // 右侧列表元素变化
    function dataChange(data) {
        for (let item in props.columns) {
            const key = props.columns[item].key;
            props.columns[item].visible = !data.includes(key);
        }
    }

    // 打开显隐列dialog
    function showColumn() {
        open.value = true;
    }

    if (props.showColumnsType == 'transfer') {
        // 显隐列初始默认隐藏列
        for (let item in props.columns) {
            if (props.columns[item].visible === false) {
                value.value.push(parseInt(item));
            }
        }
    }

    // 勾选
    function checkboxChange(event, label) {
        props.columns.filter(item => item.label == label)[0].visible = event;
    }

</script>

<style lang='scss' scoped>
    :deep(.el-transfer__button) {
        border-radius: 50%;
        display: block;
        margin-left: 0px;
    }

    :deep(.el-transfer__button:first-child) {
        margin-bottom: 10px;
    }

    :deep(.el-dropdown-menu__item) {
        line-height: 30px;
        padding: 0 17px;
    }

    .hov {
        display: flex;
        align-items: center;
    }
</style>
