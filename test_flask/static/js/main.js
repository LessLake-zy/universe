// 在Vue实例创建前获取初始数据
const initialDataElement = document.getElementById('initial-data');
const initialData = initialDataElement ? JSON.parse(initialDataElement.value) : [];

new Vue({
    el: '#app',
    data() {
        return {
            records: initialData,
            selectAll: false,
            dialogVisible: false,
            dialogTitle: '新增记录',
            formData: {
                name: '',
                gender: '',
                hometown: '',
                remarks: ''
            },
            isEdit: false,
            editIndex: -1
        }
    },
    methods: {
        showAddDialog() {
            this.dialogTitle = '新增记录';
            this.isEdit = false;
            this.clearForm();
            this.dialogVisible = true;
        },
        
        showEditDialog() {
            const selectedRecord = this.records.find(record => record.checked);
            if (!selectedRecord) {
                alert('请选择要修改的记录');
                return;
            }
            
            this.dialogTitle = '修改记录';
            this.isEdit = true;
            this.editIndex = this.records.indexOf(selectedRecord);
            this.formData = { ...selectedRecord };
            this.dialogVisible = true;
        },
        
        closeDialog() {
            this.dialogVisible = false;
            this.clearForm();
        },
        
        clearForm() {
            this.formData = {
                name: '',
                gender: '',
                hometown: '',
                remarks: ''
            };
        },
        
        toggleAll() {
            this.records.forEach(record => {
                record.checked = this.selectAll;
            });
        },
        
        async submitForm() {
            const url = this.isEdit ? '/update' : '/add';
            const data = { ...this.formData };
            
            if (this.isEdit) {
                const selectedRecord = this.records.find(record => record.checked);
                if (!selectedRecord) {
                    alert('请选择要修改的记录');
                    return;
                }
                data.index = this.records.indexOf(selectedRecord);
            }
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    if (result.status === 'success') {
                        this.dialogVisible = false;
                        this.clearForm();
                        location.reload();
                    } else {
                        alert(result.error || '操作失败，请重试');
                    }
                } else {
                    const error = await response.json();
                    alert(error.error || '操作失败，请重试');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('操作失败，请重试');
            }
        },
        
        async deleteRecord() {
            const selectedRecord = this.records.find(record => record.checked);
            if (!selectedRecord) {
                alert('请选择要删除的记录');
                return;
            }

            if (!confirm('确定要删除选中的记录吗？')) {
                return;
            }

            const index = this.records.indexOf(selectedRecord);
            
            try {
                const response = await fetch('/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ index })
                });
                
                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }
});