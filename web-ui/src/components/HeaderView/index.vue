<template>
    <div class="headerView">
        <el-row :gutter="20" style="margin: 0px;">
            <el-col :span="8" style="display: flex;align-items: center;">
                <div
                        v-if="!!iconClass"
                        :style="{ backgroundColor: iconColor }"
                        class="headerView__icon">
                    <svg-icon :icon-class="iconClass" style="font-size: 24px; color: #333; margin-top:4px;" />
                </div>
                <div class="headerView__label">
                    <slot v-if="$slots.label" name="label"/>
                    <template v-else>{{ label }}
                        <slot name="otherLabel"/>
                    </template>
                </div>
            </el-col>
            <el-col :span="16">
                <div :style="{ top: ftTop }" class="headerView__ft">
                    <slot name="ft"/>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="24" class="headerView__bottom" style="margin-left: 0px;margin-right: 0px; flex-direction: row;">
            <el-col style="width: 320px; flex-shrink: 0; margin-top:0px; flex: none;">
                <el-input
                    v-if="showSearch"
                    v-model="search"
                    :placeholder="placeholder"
                    v-bind="inputAttr"
                    class="headerView__search"
                    @input="inputChange"
                    @keyup.enter.native="searchClick">
                    <template #suffix>
                        <el-button class="searchBut" icon="search" @click="searchClick"></el-button>
                    </template>
                </el-input>
            </el-col>
            <el-col :span="14" style=" padding:0px; margin:0px;">
                
            </el-col>
            <el-col :span="6" style="width:370px; flex:none; padding:0px; margin:0px;">
                <div style="text-algin: right; float: right;">
                    <el-row>
                        <slot name="bottom-ft"/>
                    </el-row>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script setup name="HeaderView">
    const props = defineProps({
        iconClass: {
            type: String,
            default: ''
        },
        iconColor: String,
        label: String,
        // value: String,
        showSearch: {
            type: Boolean,
            default: false
        },
        placeholder: {
            type: String,
            default: '请输入内容'
        },
        ftTop: {
            type: String,
            default: '8'
        },

        content: [String, Number],

        inputAttr: {
            type: Object,
            default: () => {
            }
        }
    })

    const {iconClass, iconColor, label, showSearch, placeholder, ftTop, content, inputAttr} = toRefs(props)

    const search = ref(null)

    watch(() => props.content, (newVal) => {
        if (search.value != props.content) {
            search.value = props.content
        }
    })

    const emits = defineEmits(['update:content', 'search']);

    const inputChange = () => {
        emits("update:content", search.value);
    }

    const searchClick = () => {
        emits("search", search.value);
    }

</script>

<style lang="scss" scoped>
    .headerView {
        position: relative;

        &__icon {
            width: 30px;
            height: 30px;
            margin-right: 10px;
            line-height: 30px;
            text-align: center;
            border-radius: 3px;

            .wk {
                font-size: 18px;
                color: white;
            }
        }

        &__label {
            font-size: 24px;
            font-weight: 500;
            color: #172b4d;
        }

        &__search {
            // position: absolute;
            // top: 0;
            // left: 50%;
            width: 300px;
            // margin-top:5px;

            &.searchBut, .el-button {
                background: none;
                border: none;
                font-size: 16px;
                padding: 0px 10px 0px 10px;
                margin: 0px;
                cursor: pointer;
                line-height: 30px;
                height: 30px;
                background-color: #dfe1e6;
            }
        }

        &__ft {
            position: absolute;
            right: 0;
        }

        &__bottom {
            margin-top: 16px;
        }

    }
</style>