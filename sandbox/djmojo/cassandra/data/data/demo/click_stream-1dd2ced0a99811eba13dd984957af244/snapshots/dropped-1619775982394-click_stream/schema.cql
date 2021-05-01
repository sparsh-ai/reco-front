CREATE TABLE IF NOT EXISTS demo.click_stream (
	pk text,
	created_at timestamp,
	client_ip text,
	cookie_id text,
	event_name text,
	item_id text,
	url text,
	PRIMARY KEY (pk, created_at))
	WITH ID = 1dd2ced0-a998-11eb-a13d-d984957af244
	AND CLUSTERING ORDER BY (created_at ASC)
	AND bloom_filter_fp_chance = 0.01
	AND dclocal_read_repair_chance = 0.1
	AND crc_check_chance = 1.0
	AND default_time_to_live = 0
	AND gc_grace_seconds = 864000
	AND min_index_interval = 128
	AND max_index_interval = 2048
	AND memtable_flush_period_in_ms = 0
	AND read_repair_chance = 0.0
	AND speculative_retry = '99PERCENTILE'
	AND comment = ''
	AND caching = { 'keys': 'ALL', 'rows_per_partition': 'NONE' }
	AND compaction = { 'max_threshold': '32', 'min_threshold': '4', 'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy' }
	AND compression = { 'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor' }
	AND cdc = false
	AND extensions = {  };
CREATE INDEX IF NOT EXISTS click_stream_cookie_id_idx ON demo.click_stream (cookie_id);
CREATE INDEX IF NOT EXISTS click_stream_event_name_idx ON demo.click_stream (event_name);
CREATE INDEX IF NOT EXISTS click_stream_item_id_idx ON demo.click_stream (item_id);
