<template>
  <div class="app-container">
    <header-view
      :ftTop="'8'"
      placeholder="请输入字典名称"
      show-search
      :iconClass="'dict'"
      label="字典管理"
      @search="handleQuery"
    >
      <template v-slot:ft>
        <el-button type="primary" @click="handleAdd">添加新字典</el-button>
        <el-dropdown
          v-if="headerMoreHandle.length > 0"
          trigger="click"
          style="margin-left: 5px; margin-right: 10px"
          @command="headerMoreHandleClick"
        >
          <el-button color="#f1f1f1">
            <el-icon size="20">
              <more-filled />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                v-for="(item, index) in headerMoreHandle"
                :key="index"
                :icon="item.icon"
                :command="item.type"
              >
                {{ item.name }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-slot:bottom-ft>
        <RefreshView ref="queryRef" style="margin-right: 20px" @click="resetQuery"></RefreshView>
          <el-button
                        type="danger"
                        plain
                        icon="Refresh"
                        @click="handleRefreshCache"
                        v-hasPermi="['system:dict:remove']"
                >刷新缓存
                </el-button>
        <!-- <ShowFilter ></ShowFilter> -->
      </template>
    </header-view>

    <el-row :gutter="20" style="margin: 15px 0px">
        <el-col :span="24">
        <el-table v-loading="loading" :data="typeList" @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="55" align="center"/>
            <el-table-column label="字典编号" align="center" prop="dictId" width="100"/>
            <el-table-column label="字典名称" align="center" prop="dictName" :show-overflow-tooltip="true"/>
            <el-table-column label="字典类型" align="center" :show-overflow-tooltip="true">
                <template #default="scope">
                    <router-link :to="'/system/dictdata?dictId=' + scope.row.dictId" class="link-type">
                        <span>{{ scope.row.dictName }}</span>
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column label="状态" align="center" prop="status">
                <template #default="scope">
                    <DictTag :options="sys_normal_disable" :value="scope.row.status"/>
                </template>
            </el-table-column>
            <el-table-column label="备注" align="center" prop="remark" :show-overflow-tooltip="true"/>
            <el-table-column label="创建时间" align="center" prop="createTime" width="180">
                <template #default="scope">
                    <span>{{ parseTime(scope.row.createTime) }}</span>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" width="160" class-name="small-padding fixed-width">
                <template #default="scope">
                    <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                               v-hasPermi="['system:dict:edit']">修改
                    </el-button>
                    <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                               v-hasPermi="['system:dict:remove']">删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <div class="p-contianer">
            <pagination
                :page-sizes="[12, 20, 30, 40, 50, 100]"
                v-show="total > 0"
                :total="total"
                v-model:page="queryParams.pageNum"
                v-model:limit="queryParams.pageSize"
                     @pagination="getList"
                />
        </div>
        </el-col>
    </el-row>

  </div>
</template>

<script setup>
import HeaderView from "@/components/HeaderView";
// import DetailViews from "./components/detail.vue";
// import CreateViews from "./components/create.vue";
import ShowFilter from '@/components/showFilter'
import RefreshView from '@/components/RefreshView'
import DictTag from "@/components/dictTag";
import useDictStore from "@/store/modules/dict";
import {
  listType,
  getType,
  delType,
  addType,
  updateType,
  refreshCache,
} from "@/api/system/dict/type";

const { proxy } = getCurrentInstance();
const { sys_normal_disable } = proxy.useDict("sys_normal_disable");

// const ds = useDictStore.getDict("sys_normal_disable")

// console.log("ds", ds)

console.log("1", sys_normal_disable)
console.log("2", typeof(sys_normal_disable))


const typeList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const dateRange = ref([]);
const headerMoreHandle = ref([
    {
        icon: 'import',
        name: '导入',
        type: 'import'
    },
    {
        icon: 'export',
        name: '导出',
        type: 'export'
    }
])
const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 14,
    dictName: undefined,
    dictType: undefined,
    status: undefined,
  },
  rules: {
    dictName: [{ required: true, message: "字典名称不能为空", trigger: "blur" }],
    dictType: [{ required: true, message: "字典类型不能为空", trigger: "blur" }],
  },
});

const { queryParams, form, rules } = toRefs(data);

/** 查询字典类型列表 */
function getList() {
  loading.value = true;
  listType(proxy.addDateRange(queryParams.value, dateRange.value)).then((response) => {
    typeList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    dictId: undefined,
    dictName: undefined,
    dictType: undefined,
    status: "0",
    remark: undefined,
  };
  proxy.resetForm("dictRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
//   dateRange.value = [];
//   proxy.resetForm("queryRef");
  handleQuery();
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加字典类型";
}

/** 多选框选中数据 */
function handleSelectionChange(selection) {
  ids.value = selection.map((item) => item.dictId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const dictId = row.dictId || ids.value;
  getType(dictId).then((response) => {
    form.value = response.data;
    open.value = true;
    title.value = "修改字典类型";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["dictRef"].validate((valid) => {
    if (valid) {
      if (form.value.dictId != undefined) {
        updateType(form.value).then((response) => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addType(form.value).then((response) => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const dictIds = row.dictId || ids.value;
  proxy.$modal
    .confirm('是否确认删除字典编号为"' + dictIds + '"的数据项？')
    .then(function () {
      return delType(dictIds);
    })
    .then(() => {
      getList();
      proxy.$modal.msgSuccess("删除成功");
    })
    .catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download(
    "system/dict/type/export",
    {
      ...queryParams.value,
    },
    `dict_${new Date().getTime()}.xlsx`
  );
}

/** 刷新缓存按钮操作 */
function handleRefreshCache() {
  refreshCache().then(() => {
    proxy.$modal.msgSuccess("刷新成功");
    useDictStore().cleanDict();
  });
}

function headerMoreHandleClick (command)  {
    if (command == 'export') {
        //导入
        console.log("导入")
    } else if (command == 'import') {
        //导出
        console.log("导出")
    }
}

getList();
</script>
