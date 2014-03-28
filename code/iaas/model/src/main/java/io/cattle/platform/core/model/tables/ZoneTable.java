/**
 * This class is generated by jOOQ
 */
package io.cattle.platform.core.model.tables;

/**
 * This class is generated by jOOQ.
 */
@javax.annotation.Generated(value    = { "http://www.jooq.org", "3.3.0" },
                            comments = "This class is generated by jOOQ")
@java.lang.SuppressWarnings({ "all", "unchecked", "rawtypes" })
public class ZoneTable extends org.jooq.impl.TableImpl<io.cattle.platform.core.model.tables.records.ZoneRecord> {

	private static final long serialVersionUID = -115130198;

	/**
	 * The singleton instance of <code>cattle.zone</code>
	 */
	public static final io.cattle.platform.core.model.tables.ZoneTable ZONE = new io.cattle.platform.core.model.tables.ZoneTable();

	/**
	 * The class holding records for this type
	 */
	@Override
	public java.lang.Class<io.cattle.platform.core.model.tables.records.ZoneRecord> getRecordType() {
		return io.cattle.platform.core.model.tables.records.ZoneRecord.class;
	}

	/**
	 * The column <code>cattle.zone.id</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.Long> ID = createField("id", org.jooq.impl.SQLDataType.BIGINT.nullable(false), this, "");

	/**
	 * The column <code>cattle.zone.name</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.String> NAME = createField("name", org.jooq.impl.SQLDataType.VARCHAR.length(255), this, "");

	/**
	 * The column <code>cattle.zone.account_id</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.Long> ACCOUNT_ID = createField("account_id", org.jooq.impl.SQLDataType.BIGINT, this, "");

	/**
	 * The column <code>cattle.zone.kind</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.String> KIND = createField("kind", org.jooq.impl.SQLDataType.VARCHAR.length(255).nullable(false), this, "");

	/**
	 * The column <code>cattle.zone.uuid</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.String> UUID = createField("uuid", org.jooq.impl.SQLDataType.VARCHAR.length(128).nullable(false), this, "");

	/**
	 * The column <code>cattle.zone.description</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.String> DESCRIPTION = createField("description", org.jooq.impl.SQLDataType.VARCHAR.length(1024), this, "");

	/**
	 * The column <code>cattle.zone.state</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.String> STATE = createField("state", org.jooq.impl.SQLDataType.VARCHAR.length(128).nullable(false), this, "");

	/**
	 * The column <code>cattle.zone.created</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.util.Date> CREATED = createField("created", org.jooq.impl.SQLDataType.TIMESTAMP.asConvertedDataType(new io.cattle.platform.db.jooq.converter.DateConverter()), this, "");

	/**
	 * The column <code>cattle.zone.removed</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.util.Date> REMOVED = createField("removed", org.jooq.impl.SQLDataType.TIMESTAMP.asConvertedDataType(new io.cattle.platform.db.jooq.converter.DateConverter()), this, "");

	/**
	 * The column <code>cattle.zone.remove_time</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.util.Date> REMOVE_TIME = createField("remove_time", org.jooq.impl.SQLDataType.TIMESTAMP.asConvertedDataType(new io.cattle.platform.db.jooq.converter.DateConverter()), this, "");

	/**
	 * The column <code>cattle.zone.data</code>.
	 */
	public final org.jooq.TableField<io.cattle.platform.core.model.tables.records.ZoneRecord, java.util.Map<String,Object>> DATA = createField("data", org.jooq.impl.SQLDataType.CLOB.length(65535).asConvertedDataType(new io.cattle.platform.db.jooq.converter.DataConverter()), this, "");

	/**
	 * Create a <code>cattle.zone</code> table reference
	 */
	public ZoneTable() {
		this("zone", null);
	}

	/**
	 * Create an aliased <code>cattle.zone</code> table reference
	 */
	public ZoneTable(java.lang.String alias) {
		this(alias, io.cattle.platform.core.model.tables.ZoneTable.ZONE);
	}

	private ZoneTable(java.lang.String alias, org.jooq.Table<io.cattle.platform.core.model.tables.records.ZoneRecord> aliased) {
		this(alias, aliased, null);
	}

	private ZoneTable(java.lang.String alias, org.jooq.Table<io.cattle.platform.core.model.tables.records.ZoneRecord> aliased, org.jooq.Field<?>[] parameters) {
		super(alias, io.cattle.platform.core.model.CattleTable.CATTLE, aliased, parameters, "");
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public org.jooq.Identity<io.cattle.platform.core.model.tables.records.ZoneRecord, java.lang.Long> getIdentity() {
		return io.cattle.platform.core.model.Keys.IDENTITY_ZONE;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public org.jooq.UniqueKey<io.cattle.platform.core.model.tables.records.ZoneRecord> getPrimaryKey() {
		return io.cattle.platform.core.model.Keys.KEY_ZONE_PRIMARY;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public java.util.List<org.jooq.UniqueKey<io.cattle.platform.core.model.tables.records.ZoneRecord>> getKeys() {
		return java.util.Arrays.<org.jooq.UniqueKey<io.cattle.platform.core.model.tables.records.ZoneRecord>>asList(io.cattle.platform.core.model.Keys.KEY_ZONE_PRIMARY, io.cattle.platform.core.model.Keys.KEY_ZONE_IDX_ZONE_UUID);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public java.util.List<org.jooq.ForeignKey<io.cattle.platform.core.model.tables.records.ZoneRecord, ?>> getReferences() {
		return java.util.Arrays.<org.jooq.ForeignKey<io.cattle.platform.core.model.tables.records.ZoneRecord, ?>>asList(io.cattle.platform.core.model.Keys.FK_ZONE__ACCOUNT_ID);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public io.cattle.platform.core.model.tables.ZoneTable as(java.lang.String alias) {
		return new io.cattle.platform.core.model.tables.ZoneTable(alias, this);
	}

	/**
	 * Rename this table
	 */
	public io.cattle.platform.core.model.tables.ZoneTable rename(java.lang.String name) {
		return new io.cattle.platform.core.model.tables.ZoneTable(name, null);
	}
}