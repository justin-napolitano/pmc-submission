import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.BigtableColumn;
import com.google.cloud.bigquery.BigtableColumnFamily;
import com.google.cloud.bigquery.BigtableOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;
import org.apache.commons.codec.binary.Base64;

// Sample to queries an external bigtable data source using a temporary table
public class QueryExternalBigtableTemp {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String bigtableInstanceId = "MY_INSTANCE_ID";
    String bigtableTableName = "MY_BIGTABLE_NAME";
    String bigqueryTableName = "MY_TABLE_NAME";
    String sourceUri =
        String.format(
            "https://googleapis.com/bigtable/projects/%s/instances/%s/tables/%s",
            projectId, bigtableInstanceId, bigtableTableName);
    String query = String.format("SELECT * FROM %s ", bigqueryTableName);
    queryExternalBigtableTemp(bigqueryTableName, sourceUri, query);
  }

  public static void queryExternalBigtableTemp(String tableName, String sourceUri, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      BigtableColumnFamily.Builder statsSummary = BigtableColumnFamily.newBuilder();

      // Configuring Columns
      BigtableColumn connectedCell =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_cell".getBytes()))
              .setFieldName("connected_cell")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn connectedWifi =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_wifi".getBytes()))
              .setFieldName("connected_wifi")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn osBuild =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("os_build".getBytes()))
              .setFieldName("os_build")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();

      // Configuring column family and columns
      statsSummary
          .setColumns(ImmutableList.of(connectedCell, connectedWifi, osBuild))
          .setFamilyID("stats_summary")
          .setOnlyReadLatest(true)
          .setEncoding("TEXT")
          .setType("STRING")
          .build();

      // Configuring BigtableOptions is optional.
      BigtableOptions options =
          BigtableOptions.newBuilder()
              .setIgnoreUnspecifiedColumnFamilies(true)
              .setReadRowkeyAsString(true)
              .setColumnFamilies(ImmutableList.of(statsSummary.build()))
              .build();

      // Configure the external data source and query job.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, options).build();
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addTableDefinition(tableName, externalTable)
              .build();

      // Example query
      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external temporary table performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}