<template>
    <div class="">
        <el-tooltip class="item" effect="dark" content="显隐列" placement="top">
            <el-dropdown trigger="click" :hide-on-click="false">
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
    </div>
</template>

<script setup name="ShowFilter">
    const props = defineProps({
        value: {},
        /* 显隐列信息 */
        columns: {
            type: Array,
        },
        /* 显隐列类型（transfer穿梭框、checkbox复选框） */
        showColumnsType: {
            type: String,
            default: "checkbox",
        }
    })

    // 是否显示弹出层
    const open = ref(false);
    const openSc = ref(false);

    // 打开显隐列dialog
    function showColumn() {
        open.value = true;
    }

    function dataChange(data) {
        for (let item in props.columns) {
            const key = props.columns[item].key;
            props.columns[item].visible = !data.includes(key);
        }
    }

    const {columns, showColumnsType} = toRefs(props)


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