package com.ruyou.web.base.project.dao.excel;

import com.ruyou.web.base.project.dao.base.BaseDao;
import com.ruyou.web.base.project.model.excel.ContractInsuranceType;
import org.springframework.stereotype.Repository;

/**
 * @Author: Lianbb
 * @Date: 2020/4/23 14:48
 */
@Repository
public class ContractInsuranceTypeDao extends BaseDao<ContractInsuranceType> {

    public void deleteItemByNo(String contractNo,int baseId){
        jdbcTemplate.update("delete from "+getTableName()+" where contract_no=? and base_id=?",new Object[]{contractNo,baseId});
    }

}
