<template>
    <el-drawer
            class="drawerview"
            v-model="drawerdef"
            size="80%"
            :close-on-click-modal="false"
            :show-close="false"
            direction="rtl"
            :modal="false"
            :before-close="handleClose"
    >
        <template v-show="titleShow" #header>
            <h4>{{ title }}</h4>
        </template>
        <template #default>
            <el-button
                    v-if="showClose"
                    class="close-btn"
                    type="primary"
                    icon="DArrowRight"
                    @click="handleClose"
            />
            <div class="DrawerView">
                <slot name="content"/>
            </div>
        </template>
        <template v-if="footerShow" #footer>
            <div class="dialog-footer">
                <el-button type="primary"> 确认提交</el-button>
                <el-button @click="handleClose">取消</el-button>
            </div>
        </template>
    </el-drawer>
</template>

<script setup name="DrawerView">
    import {toRefs} from "vue";

    const props = defineProps({
        title: {
            type: String,
            default: "",
        },
        /* 是否显示检索图标 */
        value: {
            type: Boolean,
            default: false,
        },
        titleShow: {
            type: Boolean,
            default: false,
        },
        footerShow: {
            type: Boolean,
            default: false,
        },
        showClose: {
            type: Boolean,
            default: true,
        },
    });

    const {title, titleShow, footerShow, showClose} = toRefs(props);

    const drawerdef = computed({
        get: () => props.value,
        set: (val) => {
            emit("update:value", val);
        },
    });

    const emit = defineEmits(["update:value", "closeHandle"]);

    const handleClose = () => {
        emit("closeHandle", false);
    };

    // const handleClose = (done) => {
    //   if (loading.value) {
    //     return
    //   }
    //   ElMessageBox.confirm('Do you want to submit?')
    //     .then(() => {
    //       loading.value = true
    //       timer = setTimeout(() => {
    //         done()
    //         // 动画关闭需要一定的时间
    //         setTimeout(() => {
    //           loading.value = false
    //         }, 400)
    //       }, 2000)
    //     })
    //     .catch(() => {
    //       // catch error
    //     })
    // }
</script>

<style lang="scss" scoped>
    $--but-color-primary: #0858a8;
    .drawerview {
        overflow: initial;
    }

    .el-drawer {
        overflow: initial;
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
        height: 36px;
        font-size: 26px;

        i {
            margin-right: 0;
            font-size: 26px;
        }
    }
</style>
