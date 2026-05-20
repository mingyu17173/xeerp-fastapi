<template>
    <el-dialog
            v-model="open"
            :title="title"
            width="500"
            modal
            :before-close="handleClose">
        <div class="importVis">
            <el-upload
                    ref="uploadRef"
                    :limit="1"
                    accept=".xlsx, .xls"
                    :headers="headers"
                    :action="url + '?updateSupport=' + updateSupport"
                    :disabled="isUploading"
                    :on-progress="handleFileUploadProgress"
                    :on-success="handleFileSuccess"
                    :auto-upload="true"
                    drag>
                <el-icon class="el-icon--upload">
                    <upload-filled/>
                </el-icon>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <template #tip>
                    <div class="el-upload__tip text-center">
                        <div class="el-upload__tip">
                            <el-checkbox v-model="updateSupport"/>
                            是否更新已经存在的客户数据
                        </div>
                        <span>仅允许导入xls、xlsx格式文件。</span>
                        <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;"
                                 @click="importTemplate">下载模板
                        </el-link>
                    </div>
                </template>
            </el-upload>
        </div>
        <!-- <template #footer>
        </template> -->
    </el-dialog>
</template>

<script setup>
    import {ref, reactive, nextTick, getCurrentInstance} from "vue";
    import {getToken} from "@/utils/auth";

    const {proxy} = getCurrentInstance();

    const props = defineProps({
        modelValue: {
            type: Boolean,
            default: false
        }
    })
    const emit = defineEmits()

    const upload = reactive({
        // 是否显示弹出层（用户导入）
        open: false,
        // 弹出层标题（用户导入）
        title: "文件导入",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的用户数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: {Authorization: "Bearer " + getToken()},
        // 上传的地址
        url: import.meta.env.VITE_APP_BASE_API + "/erp/partner/import"
    });

    const {open, title, isUploading, updateSupport, headers, url} = toRefs(upload)

    watch(() => props.modelValue, value => upload.open = value)

    const handleClose = (res) => {
        emit("update:modelValue", false)
    }

    /** 下载模板操作 */
    const importTemplate = () => {
        proxy.download("/erp/partner/export", {}, `user_template_${new Date().getTime()}.xlsx`);
    };

    /**文件上传中处理 */
    const handleFileUploadProgress = (event, file, fileList) => {
        upload.isUploading = true;
    };
    /** 文件上传成功处理 */
    const handleFileSuccess = (response, file, fileList) => {
        upload.open = false;
        upload.isUploading = false;
        proxy.$refs["uploadRef"].handleRemove(file);
        proxy.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", {dangerouslyUseHTMLString: true});
        getList();
    };

</script>
<style>
    .importVis {
        width: 100%;
    }
</style>