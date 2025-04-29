$(document).ready(function() {
    // 显示新增对话框
    function showAddDialog() {
        $('#dialogTitle').text('新增记录');
        $('#recordDialog').show();
        clearForm();
    }

    // 显示编辑对话框
    function showEditDialog() {
        const $checked = $('.record-checkbox:checked');
        if (!$checked.length) {
            alert('请选择要修改的记录');
            return;
        }
        
        const $row = $checked.closest('tr');
        $('#dialogTitle').text('修改记录');
        $('#name').val($row.find('td:eq(1)').text());
        $('#gender').val($row.find('td:eq(2)').text());
        $('#hometown').val($row.find('td:eq(3)').text());
        $('#remarks').val($row.find('td:eq(4)').text());
        
        $('#recordDialog').show();
    }

    // 关闭对话框
    function closeDialog() {
        $('#recordDialog').hide();
    }

    // 清空表单
    function clearForm() {
        $('#recordForm')[0].reset();
    }

    // 全选/取消全选
    function toggleAll() {
        const isChecked = $('#selectAll').prop('checked');
        $('.record-checkbox').prop('checked', isChecked);
    }

    // 表单提交处理
    $('#recordForm').on('submit', function(e) {
        e.preventDefault();
        
        const data = {
            name: $('#name').val(),
            gender: $('#gender').val(),
            hometown: $('#hometown').val(),
            remarks: $('#remarks').val()
        };

        const isEdit = $('#dialogTitle').text() === '修改记录';
        const url = isEdit ? '/update' : '/add';
        
        if (isEdit) {
            const $checked = $('.record-checkbox:checked');
            const index = $checked.closest('tr').index();
            data.index = index;
        }

        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                location.reload();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    // 删除记录
    function deleteRecord() {
        const $checked = $('.record-checkbox:checked');
        if (!$checked.length) {
            alert('请选择要删除的记录');
            return;
        }

        if (!confirm('确定要删除选中的记录吗？')) {
            return;
        }

        const index = $checked.closest('tr').index();
        
        $.ajax({
            url: '/delete',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ index: index }),
            success: function() {
                location.reload();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    // 绑定按钮事件
    $('#addBtn').on('click', showAddDialog);
    $('#editBtn').on('click', showEditDialog);
    $('#deleteBtn').on('click', deleteRecord);
    $('#cancelBtn').on('click', closeDialog);
    $('#selectAll').on('click', toggleAll);
});