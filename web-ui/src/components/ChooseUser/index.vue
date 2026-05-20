<template>
  <el-dialog
    class="selectview" 
    v-model="drawerdef"
    :title="title"
    width="800"
    :close-on-click-modal="false"
    :show-close="false"
    :modal="true"
    :lock-scroll="true"
    append-to-body  
    :before-close="handleClose">
    <template #header>
      <h4 style="margin: 0px; font-size: 20px; font-weight: 500;">{{ title }}</h4>
    </template>
    <div class="mainview">
      <div class="main-left">
        <div class="main-top">
          <el-input
            v-model="dialogSearch"
            style="width: 100%"
            placeholder="请输入关键词"
            :suffix-icon="Search"
          />
        </div>
        <div class="main-body-wrap">
          <el-table v-loading="loading" :data="userList" border stripe show-header highlight-current-row height="470" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="50" align="center"/>
            <el-table-column label="用户名称" align="center" key="userName" prop="userName" />
            <el-table-column label="用户昵称" align="center" key="nickName" prop="nickName" />
          </el-table>
        </div>
      </div>
      <div class="main-right">
        <div class="main-top">
          已选：{{ changeItem.length }} 员工
        </div>
        <div class="main-body-wrap">
          <el-tag v-for="tag in changeItem" :key="tag.nickName" closable @close="handleTagClose(tag)" style="margin-right: 10px; margin-bottom:10px;">
            {{ tag.nickName }}
          </el-tag>
        </div>
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button :loading="loading" type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="handleClose">取 消</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
  import { Search } from '@element-plus/icons-vue'
  import { listUser } from "@/api/system/user";
  const {proxy} = getCurrentInstance();
  
  const props = defineProps({
      title: {
          type: String,
          default: '选择'
      },
      /* 是否显示检索图标 */
      value: {
          type: Boolean,
          default: false,
      }
  })
  const  { title } = toRefs(props);

  const emit = defineEmits(['update:value', 'closeHandle', 'onChange']);

  const drawerdef = computed({
    get: () => props.value,
    set: (val) => {
      emit('update:value', val)
    }
  });

  const dialogSearch = ref('')
  const userList = ref([])
  const loading = ref(false)
  const dateRange = ref([])
  const total = ref(0)
  const queryParams = ref({
      pageNum: 1,
      pageSize: 100,
      userName: undefined,
      phonenumber: undefined,
      status: undefined,
      dept_id: undefined
  })
  const ids = ref([]);
  const single = ref(true)
  const multiple = ref(true)
  const changeItem = ref([])


  // 取消按钮
  const handleClose = () => {
      emit('closeHandle', false);
      
  }

  const submitForm = () => {
    emit('onChange', changeItem.value);
    emit('closeHandle', false);
    emit('update:value', false);
    // if (changeItem.value.length > 0) {
    //   return
    // }
    // proxy.$refs["partnerRef"].validate((valid) => {
    //     if (valid) {
    //       console.log("验证通过")
    //     } else { 
    //       console.log("验证失败")
    //     }
    // });
  }

  function handleSelectionChange(selection) {
    changeItem.value = selection
    ids.value = selection.map(item => item.user_id);
    single.value = selection.length != 1;
    multiple.value = !selection.length;
  };

  function getList() {
    loading.value = true;
    listUser(proxy.addDateRange(queryParams.value, dateRange.value)).then(res => {
        loading.value = false;
        userList.value = res.rows;
        total.value = res.total;
    });
      
  };

  const handleTagClose = (tag) => {
    // 删除已选项
    changeItem.value.splice(changeItem.value.indexOf(tag), 1)
  }

  onMounted(() => {
      getList();
  });
</script>

<style lang="scss">
.selectview {
  .el-dialog {
    &__body {
      height: 60vh;
      overflow: hidden;
      overflow-y: auto;
      margin: 0px 0px;
      padding: 10px 20px;
    }
    &__title {
      color: #172b4d;
      font-size: 18px;
      line-height: 24px;
    }
    &__footer {
      padding: 10px 20px 18px;
      text-align: right;
    } 
    
  }
  .mainview {
    border: 1px solid #dfe1e6;
    display: flex;
    height: 100%;
    .main-left {
      border-right: 1px solid #dfe1e6;
      flex: 1;
      height: 100%;
      overflow: hidden;
      .main-top {
        border-bottom: 1px solid #dfe1e6;
        line-height: 50px;
        padding: 0 16px;
        position: relative;
      }
      .main-body-wrap {
        height: calc(100% - 60px);
        padding: 14px;
        position: relative;
      }
    }
    .main-right {
      flex: 1;
      .main-top {
        border-bottom: 1px solid #dfe1e6;
        line-height: 50px;
        padding:0 16px;
        position: relative;
      }
      .main-body-wrap {
        height: calc(100% - 60px);
        padding: 14px;
        position: relative;
      }
    }
  }
}

</style>