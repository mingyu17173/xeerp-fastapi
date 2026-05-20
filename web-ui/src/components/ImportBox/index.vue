<template>
    <el-drawer v-model="drawerdef" show-close="false">
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="handleClose">Cancel1</el-button>
                <el-button type="primary">
                    Confirm1
                </el-button>
            </div>
        </template>
    </el-drawer>
</template>

<script setup name="ImportBox">

    const props = defineProps({
        /**当前双向数据绑定的值 */
        value: {
            type: Boolean,
            default: false
        },
    })
    // const emits = defineEmits(['update:showSearch', 'queryTable']);

    const emit = defineEmits(['update:value', 'closeHandle']);

    const drawerdef = computed({
        get: () => props.value,
        set: (val) => {
            emit('update:value', val)
        }
    });

    const handleClose = () => {
        emit('closeHandle', false);
    }


</script>