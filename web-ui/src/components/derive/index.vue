<template>
    <div v-if="isOpen">
        <el-dialog :title="title" v-model="openModal" width="750px" append-to-body :close-on-click-modal="false"
                   style="margin-top: 15vh!important">
            <el-steps :active="1" align-center>
                <el-step title="导出配置"/>
                <el-step title="导出完成"/>
            </el-steps>
            <div style="padding: 0 40px;margin-top: 40px;">
                <div>
                    <p style="font-weight: bold;">选择字段导出范围：</p>
                    <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选
                    </el-checkbox>
                    <el-checkbox-group v-model="checkedCities" @change="handleCheckedCitiesChange">
                        <el-checkbox v-for="city in cities" :key="city" :label="city">{{city}}</el-checkbox>
                    </el-checkbox-group>
                </div>
                <div class="mb-2 flex items-center text-sm">
                    <p style="font-weight: bold;margin-top: 24px;margin-bottom: 4px;">选择导出文件类型：</p>
                    <el-radio-group v-model="radio1" class="ml-4">
                        <el-radio label="1" size="large">xls</el-radio>
                        <el-radio label="2" size="large">csv</el-radio>
                    </el-radio-group>
                </div>
            </div>
            <template #footer>
                <div class="dialog-footer">
                    <el-button type="primary">立即导出</el-button>
                    <el-button @click="closeModal">取 消</el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    const props = defineProps({
        columlList: {
            type: Array,
        },
        isOpen: {
            type: [Boolean, String, Number],
            default: false,
        },
        title: {
            type: String,
            default: '导出客户',
        },
    })

    const checkAll = ref(false)
    const isIndeterminate = ref(true)
    const checkedCities = ref(['Shanghai', 'Beijing'])
    const cities = ['Shanghai', 'Beijing', 'Guangzhou', 'Shenzhen']
    const radio1 = ref('1')

    // 是否显示弹出层
    // const isOpen = ref(false);

    const emits = defineEmits(['update:isOpen', 'closehan']);

    // const data = reactive({
    //   form: {},
    //   queryParams: {
    //     pageNum: 1,
    //     pageSize: 10,
    //   },
    //   rules: {
    //     userName: [{ required: true, message: "用户名称不能为空", trigger: "blur" }, { min: 2, max: 20, message: "用户名称长度必须介于 2 和 20 之间", trigger: "blur" }],
    //     nickName: [{ required: true, message: "用户昵称不能为空", trigger: "blur" }],
    //     password: [{ required: true, message: "用户密码不能为空", trigger: "blur" }, { min: 5, max: 20, message: "用户密码长度必须介于 5 和 20 之间", trigger: "blur" }, { pattern: /^[^<>"'|\\]+$/, message: "不能包含非法字符：< > \" ' \\\ |", trigger: "blur" }],
    //     email: [{ type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] }],
    //     phonenumber: [{ pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/, message: "请输入正确的手机号码", trigger: "blur" }],
    //   }
    // });

    // const { queryParams, form, rules } = toRefs(data);

    const openModal = computed({
        get: () => props.isOpen,
        set: (val) => {
            emits('update:isOpen', val)
        }
    });

    // const closeModal = computed({
    //   get: () => props.isOpen,
    //   set: (val) => {
    //     emits('update:closehan', false)
    //   }
    // });
    const closeModal = () => {
        emits("closehan", false);
    }
    const handleCheckAllChange = (val) => {
        checkedCities.value = val ? cities : []
        isIndeterminate.value = false
    }
    const handleCheckedCitiesChange = (value) => {
        const checkedCount = value.length
        checkAll.value = checkedCount === cities.length
        isIndeterminate.value = checkedCount > 0 && checkedCount < cities.length
    }
</script>

<style lang='scss' scoped>
</style>

