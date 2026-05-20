<template>
    <div class="AdvancedFilter" :title="title">
        <el-tooltip class="item" effect="dark" content="高级筛选" placement="top">
            <div class="filters" @click="dialogVisible = true">
                <el-icon>
                    <Search/>
                </el-icon>
                <span v-if="value">11</span>
            </div>
        </el-tooltip>
        <el-dialog
                v-model="dialogVisible"
                :title="title"
                width="700"
                close-on-click-modal>
            <div class="">
                <slot name="content"/>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary" @click="dialogVisible = false">确认</el-button>
                    <el-button @click="dialogVisible = false">重置</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup name="AdvancedFilter">
    import {toRefs} from 'vue'

    const props = defineProps({
        title: {
            type: String,
            default: '高级筛选'
        },
        /* 是否显示检索图标 */
        value: {
            type: Boolean,
            default: false,
        }
    })

    const {title} = toRefs(props)

    const dialogVisible = ref(false)

</script>

<style lang="scss" scoped>

    .AdvancedFilter {
        position: relative;

        .filters {
            font-size: 14px;
            width: 32px;
            border-radius: 50%;
            height: 32px;
            padding: 8px;
            background-color: #FFF;
            border: 1px solid #dfe1e8;
            cursor: pointer;
            position: relative;
            margin-top: 8px;

            i {
                color: #606266;
            }

            &:hover {
                background-color: #e1edff;
                border: 1px solid #c5e1ff;

                i {
                    color: #0052cc;
                }
            }

            span {
                padding: 0px;
                z-index: 999;
                position: absolute;
                top: -8px;
                right: -9px;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: #67758a;
                font-size: 9pt;
                text-align: center;
                color: #fff;
                font-weight: 500;
                line-height: 20px;
            }
        }
    }
</style>