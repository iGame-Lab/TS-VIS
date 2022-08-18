
<template>
    <el-dialog title="登录" :visible.sync="dialogFormVisible">
        <el-form :label-position="labelPosition" label-width="150px" :model="formLabelAlign">
            <el-form-item label="userId">
                <el-input v-model="formLabelAlign.id"></el-input>
            </el-form-item>
            <el-form-item label="trainJobName">
                <el-input v-model="formLabelAlign.trainJobName"></el-input>
            </el-form-item>
            
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="confirm">确 定</el-button>
        </div>
    </el-dialog>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'
import { createNamespacedHelpers } from 'vuex'
const {
  mapMutations: mapLayoutMutations,
  mapActions: mapLayoutActions,
} = createNamespacedHelpers('layout')
export default {
    data() {
      return {
        dialogFormVisible:true,
        labelPosition: 'right',
        formLabelAlign: {
            trainJobName: 'test',
            id: 'user1'
        }
      };
    },
    methods:{
        ...mapLayoutMutations(["setParams"]),
        ...mapLayoutActions(["initWaitingPage"]),
        confirm:function(){
            this.dialogFormVisible = false
            this.$nextTick(()=>{this.setParams(this.formLabelAlign)})
            this.$nextTick(()=>{this.initWaitingPage(this.formLabelAlign)})
        }
    },

}
</script>

<style lang="less" scoped>

</style>