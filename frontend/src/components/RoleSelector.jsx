/**
 * RoleSelector
 * Props:
 *   value: string
 *   onChange: (value: string) => void
 *   disabled?: boolean
 */
function RoleSelector({ value, onChange, disabled = false }) {
    return (
        <div>
            <label className="field-label" htmlFor="target-role">
                target_role:
            </label>

            <input
                id="target-role"
                type="text"
                className="input-pixel"
                placeholder="e.g. Data Scientist"
                value={value}
                disabled={disabled}
                onChange={(event) => onChange(event.target.value)}
            />
        </div>
    );
}

export default RoleSelector;