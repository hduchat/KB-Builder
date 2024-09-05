SELECT
	app_or_dataset.*,
	team_member_permission.member_id,
	team_member_permission.operate
FROM
	(
	SELECT
		"id",
		"name",
		'DATASET' AS "type",
        d.type_child,  --  新增：从 dataset 表中获取 type_child 字段
		user_id
	FROM
		dataset d  -- 修改：为 dataset 表添加别名 "d"
	WHERE
		"user_id" = %s
    UNION
	SELECT
		"id",
		"name",
		'APPLICATION' AS "type",
        NULL AS type_child,  --  新增：为 application 类型添加 type_child 字段，并赋值为 NULL
		user_id
	FROM
		application
	WHERE
		"user_id" = %s
	) app_or_dataset
	LEFT JOIN ( SELECT * FROM team_member_permission WHERE member_id = %s ) team_member_permission ON team_member_permission.target = app_or_dataset."id"