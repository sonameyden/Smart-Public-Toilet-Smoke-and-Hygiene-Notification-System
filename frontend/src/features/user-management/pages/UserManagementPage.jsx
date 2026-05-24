import { useState } from 'react'
import { UserPlus } from 'lucide-react'
import Topbar from '../../../components/layout/Topbar'
import UsersTable from '../components/UsersTable'
import AddUserModal from '../components/AddUserModal'
import { useUsers, useCreateUser, useDeleteUser } from '../hooks/useUsers'
import Button from '../../../components/ui/Button'

const MOCK_USERS = [
  { id: '1', full_name: 'Admin User',        email: 'admin@campus.edu',       role: 'admin',       is_active: true, last_login: new Date(Date.now() - 30 * 60 * 1000).toISOString() },
  { id: '2', full_name: 'Maintenance Staff', email: 'maintenance@campus.edu', role: 'maintenance', is_active: true, last_login: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString() },
  { id: '3', full_name: 'Campus Authority',  email: 'authority@campus.edu',   role: 'viewer',      is_active: true, last_login: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString() },
  { id: '4', full_name: 'New User',          email: 'newuser@campus.edu',     role: 'viewer',      is_active: true, last_login: null },
]

export default function UserManagementPage() {
  const [showModal, setShowModal] = useState(false)

  const { data, isLoading } = useUsers()
  const { mutate: create, isPending: creating } = useCreateUser()
  const { mutate: remove } = useDeleteUser()

  const users = data ?? MOCK_USERS

  const handleCreate = (payload) => {
    create(payload, { onSuccess: () => setShowModal(false) })
  }

  return (
    <div className="flex flex-col h-full">
      <Topbar title="User Management" />

      <div className="flex-1 overflow-y-auto p-6 space-y-5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold sg-text">User Management</h2>
            <p className="text-xs sg-muted mt-0.5">Manage system users and their roles</p>
          </div>
          <Button variant="primary" size="md" onClick={() => setShowModal(true)}>
            <UserPlus size={14} />
            Add User
          </Button>
        </div>

        {isLoading ? (
          <p className="text-sm sg-muted">Loading…</p>
        ) : (
          <UsersTable
            users={users}
            onDelete={(id) => remove(id)}
          />
        )}
      </div>

      {showModal && (
        <AddUserModal
          onClose={() => setShowModal(false)}
          onSubmit={handleCreate}
          loading={creating}
        />
      )}
    </div>
  )
}
